from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import datetime

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
from socket import socket, AF_INET, SOCK_DGRAM
import os

HOST = ''
PORT = os.environ['UDP_PORT']


def background_thread():
    """Example of how to send server generated events to clients."""
    # UDP
    s = socket(AF_INET, SOCK_DGRAM)  # ソケットを用意
    s.bind((HOST, int(PORT)))  # バインドしておく

    count = 0
    while True:
        socketio.sleep(0.001)    # 単位(s)
        count += 1
        dt_now = datetime.datetime.now()

        # 受信
        msg, address = s.recvfrom(8192)
        msg = msg.decode("utf-8")
        print(f"message: {msg}\nfrom: {address}")

        socketio.emit('my_response',
                      {'data': 'to Server->' + msg, 'count': str(dt_now)})

    s.close()  # ソケットを閉じておく


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
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    # SocketIOサーバをデバッグモードで起動
    # socketio.run(app, debug=True)
    socketio.run(app, host="0.0.0.0")
