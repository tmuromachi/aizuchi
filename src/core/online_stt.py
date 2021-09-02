from __future__ import division

import re
import sys
import pathlib
import os
from socket import socket, AF_INET, SOCK_DGRAM

from google.cloud import speech

import pyaudio
from six.moves import queue
from jumanpp import jumanpp_parser
from src.web.util import text_wrapper

# base.pyのあるディレクトリの絶対パスを取得
current_dir = pathlib.Path(__file__).resolve().parent
# モジュールのあるパスを追加
sys.path.append(str(current_dir) + '/../')

# GCP認証情報
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/toshiki/data/cloud/gcp/tmuromachi-ed1cc8e5a9ae.json'

# True:逐次的に音声認識を行う, False:話者が発話を終了して認識結果が定まったら表示する
SEQUENTIAL = True

# Audio recording parameters
# 録音パラメータ
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

# UDP(server)
HOST = ''
PORT = os.environ['UDP_PORT']
# ADDRESS = "127.0.0.1" # 自分に送信
ADDRESS = "web"  # 自分に送信


class MicrophoneStream(object):
    """
    Opens a recording stream as a generator yielding the audio chunks.
    オーディオチャンクを生成するジェネレータとして録音ストリームを開きます。
    """

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # APIは現在、1チャンネル（モノラル）オーディオのみをサポートしています
            # https://goo.gl/z757pE
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            # オーディオストリームを非同期で実行して、バッファオブジェクトを埋めます。
            # これは呼び出し元のスレッドがネットワーク要求などを行うときに、入力デバイスのバッファがオーバーフローしないようにするために必要
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        # クライアントのstreaming_recognizeメソッドがプロセスの終了をブロックしないように、ジェネレーターに終了するように通知します。
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """
        Continuously collect data from the audio stream, into the buffer.
        オーディオストリームからバッファにデータを継続的に収集します。
        """
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            # ブロッキングget()を使用して、データのチャンクが少なくとも1つあることを確認し、
            # チャンクがNoneの場合は反復を停止して、オーディオストリームの終了を示します。
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            # ここで、まだバッファリングされている他のデータをすべて消費します。
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)


def listen_print_loop(responses, s):
    """
    Iterates through server responses and prints them.
    サーバーの応答を繰り返し、それらを出力します。

    The responses passed is a generator that will block until a response
    is provided by the server.
    渡される応答は、サーバーから応答が提供されるまでブロックするジェネレーターです。

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.
    各応答には複数の結果が含まれる場合があり、各結果には含まれる場合があります
    複数の選択肢; 詳細については、https：//goo.gl/tjCPAUをご覧ください。
    ここで私たちは上位の結果の上位の選択肢の文字起こしのみを印刷します。

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    この場合、中間結果に対しても回答が提供されます。 応答が暫定的なものである場合は、応答が最終的なものになるまで、
    次の結果がそれを上書きできるように、応答の最後に改行を印刷します。
    最後の1つについては、改行を印刷して、完成した文字起こしを保持します。
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        # 「結果」リストは連続しています。 ストリーミングの場合、最初の結果のみが考慮されます。
        # これは、「is_final」になると、次の発話の考慮に進むためです。
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        # トップオルタナティヴの文字起こしを表示します。
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        # 中間結果を表示しますが、行の終わりにキャリッジリターンがあるため、後続の行で上書きされます。
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        # 前の結果がこれよりも長かった場合は、前の結果を上書きするためにいくつかの余分なスペースを印刷する必要があります
        overwrite_chars = " " * (num_chars_printed - len(transcript))

        # 逐次予測の場合は結果が確定していない段階で表示する
        if SEQUENTIAL:
            # 音声認識結果表示部分
            print(transcript)
            wrap_transcript = text_wrapper(transcript, 30)
            if jumanpp_parser(transcript):    # 相槌箇所であるかどうか
                wrap_transcript = wrap_transcript + '<br><span style="color:#AAAAAA;">' + '【相槌可能】' + '</span>'
            s.sendto(wrap_transcript.encode(), (ADDRESS, int(PORT)))
        else:
            if not result.is_final:
                sys.stdout.write(transcript + overwrite_chars + "\r")
                sys.stdout.flush()
                num_chars_printed = len(transcript)
            else:
                print(transcript + overwrite_chars)
                num_chars_printed = 0

        # Exit recognition if any of the transcribed phrases could be
        # one of our keywords.
        # 認識されたフレーズのいずれかがキーワードの1つである可能性がある場合は、認識を終了します。
        if re.search(r"認識終了", transcript, re.I):
            print("Exiting..")
            break


def main():
    s = socket(AF_INET, SOCK_DGRAM)

    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages. 言語サポートリストから選択する
    language_code = "ja-JP"  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        # 次に、応答を使用します。
        listen_print_loop(responses, s)

    s.close()


if __name__ == "__main__":
    main()
