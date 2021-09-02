from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit

from util import text_wrapper
from jumanpp import jumanpp_parser

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
# 非同期処理に使用するライブラリの指定
# `threading`, `eventlet`, `gevent`から選択可能
async_mode = None

# Flaskオブジェクトを生成し、セッション情報暗号化のキーを指定
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# Flaskオブジェクト、async_modeを指定して、SocketIOサーバオブジェクトを生成
socketio = SocketIO(app, async_mode=async_mode)
# スレッドを格納するためのグローバル変数
thread = None
thread_lock = Lock()

# UDP(client)
import os

HOST = ''
PORT = os.environ['UDP_PORT']


def background_thread(transcript):
    """Example of how to send server generated events to clients."""
    print("")


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.event
def my_event(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.event
def my_ping():
    emit('my_pong')


@socketio.event
def connect():
    # global thread
    # with thread_lock:
    #     if thread is None:
    #         thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


@socketio.on('stt_result')
def receive_transcript(stt_result):
    # 音声認識結果をクライアント側から受け取って整形/相槌判定を行う
    wrap_transcript = text_wrapper(stt_result['data'], 30)
    if jumanpp_parser(wrap_transcript):  # 相槌箇所であるかどうか
        wrap_transcript = wrap_transcript + '<br><span style="color:#AAAAAA;">' + '【相槌可能】' + '</span>'
    print(wrap_transcript)
    socketio.emit('jumanpp_parser', {'data': wrap_transcript, 'count': 0})


if __name__ == '__main__':
    # SocketIOサーバをデバッグモードで起動
    # socketio.run(app, debug=True)
    # socketio.run(app, host="0.0.0.0")
    socketio.run(app, host="0.0.0.0")
