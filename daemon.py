import socket
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class LaTeXListenHandler(FileSystemEventHandler):
    def on_modified(self, event):
        src_path = event.src_path
        p = Path(src_path)
        working_dir = str(p.parents[0])
        print('[DEBUG] modified', event)
        subprocess.Popen(['xelatex', event.src_path], cwd=working_dir)

SOCKET_PATH = "/tmp/latexlisten.sock"

if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCKET_PATH)
server.listen(1)

print("LaTeXListen Daemon listening...")

main_event_handler = LaTeXListenHandler()
active_uris = set()
observers = []
while True:
    conn, _ = server.accept()
    data = conn.recv(1024).decode()

    if data == "ping":
        conn.send(b"pong rev5")
    elif data[:6] == "listen":
        fname_raw = data[7:]
        print('[DEBUG] listen', fname_raw)
        path = Path.from_uri(fname_raw)
        if fname_raw in active_uris:
            conn.send(b"already watching")
        elif path.exists():
            active_uris.add(fname_raw)
            observer = Observer()
            observer.schedule(main_event_handler, str(path), recursive=False)
            observer.start()
            observers.append(observer)
            conn.send(b"found, observing")
        else:
            conn.send(b"not found")
    elif data == "stop":
        conn.send(b"stopping")
        break
    else:
        conn.send(b"unknown command")

    conn.close()

server.close()
