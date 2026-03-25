import socket
import os
from pathlib import Path

SOCKET_PATH = "/tmp/latexlisten.sock"

if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCKET_PATH)
server.listen(1)

print("LaTeXListen Daemon listening...")

while True:
    conn, _ = server.accept()
    data = conn.recv(1024).decode()

    if data == "ping":
        conn.send(b"pong rev3")
    elif data[:6] == "listen":
        fname_raw = data[7:]
        print('[DEBUG]', fname_raw)
        path = Path.from_uri(fname_raw)
        if path.exists():
            conn.send(b"found")
        else:
            conn.send(b"not found")
    elif data == "stop":
        conn.send(b"stopping")
        break
    else:
        conn.send(b"unknown command")

    conn.close()

server.close()
