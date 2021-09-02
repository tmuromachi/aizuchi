from socket import socket, AF_INET, SOCK_DGRAM

HOST = ''
PORT = 8000

# ソケットを用意
s = socket(AF_INET, SOCK_DGRAM)
# バインドしておく
s.bind((HOST, PORT))

while True:
    # 受信
    msg, address = s.recvfrom(8192)
    msg = msg.decode("utf-8")
    print(f"message: {msg}\nfrom: {address}")

# ソケットを閉じておく
s.close()
