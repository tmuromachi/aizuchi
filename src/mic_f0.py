import numpy as np
import pyaudio


class MicF0:
    def __init__(self):
        # マイクインプット設定
        # self.CHUNK = 1024  # 1度に読み取る音声のデータ幅
        self.CHUNK = 512  # 1度に読み取る音声のデータ幅
        self.RATE = 44100  # サンプリング周波数 16000->441000->16000
        self.update_seconds = 50  # 更新時間[ms]
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=self.RATE,
                                      input=True,
                                      frames_per_buffer=self.CHUNK)

        # 音声データの格納場所(プロットデータ)
        self.data = np.zeros(self.CHUNK)

    def update(self):
        """
        F0推定(簡易版)
        :return: F0
        """
        self.data = np.append(self.data, self.audio_input())
        if len(self.data) / 1024 > 10:
            self.data = self.data[1024:]
        self.fft_data = self.fft_amp(self.data)
        self.axis = np.fft.fftfreq(len(self.data), d=1.0 / self.RATE)
        self.plotData = self.fft_data  # 配列操作用の変数
        self.plotData[self.plotData < 5.0] = 0.0  # 1より振幅が小さいものは捨てる
        self.plotData[self.plotData > 1500.0] = 0.0  # 1500より振幅が小さいものは捨てる
        self.datamax = np.argmax(self.plotData)  # FFTされたものの一番大きいものを取り出す
        # print(datetime.datetime.now(), self.datamax, abs(self.axis[self.datamax] * 0.8))
        return abs(self.axis[self.datamax] * 0.8)

    def audio_input(self):
        ret = self.stream.read(self.CHUNK)  # 音声の読み取り(バイナリ) CHUNKが大きいとここで時間かかる
        # バイナリ → 数値(int16)に変換
        # 32768.0=2^16で割ってるのは正規化(絶対値を1以下にすること)
        ret = np.frombuffer(ret, dtype="int16") / 32768.0
        # print(ret)
        return ret

    def fft_amp(self, data):
        data = np.hamming(len(data)) * data
        data = np.fft.fft(data)
        data = np.abs(data)
        return data
