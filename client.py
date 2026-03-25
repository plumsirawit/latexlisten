import socket
import argparse
from pathlib import Path
# TEST 5
def ping(args):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect("/tmp/latexlisten.sock")

    client.send(b"ping")
    print(client.recv(1024))
    client.close()

def listen(args):
    path = Path(args.fname)
    if not path.exists():
        print('The specified path does not exist!')
        return
    resolved = path.resolve().as_uri()
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect("/tmp/latexlisten.sock")

    client.send(b"listen " + resolved.encode('utf-8'))
    print(client.recv(1024))
    client.close()

parser = argparse.ArgumentParser(
                    prog='LaTeXListen Client',
                    description='A client for the LaTeXListen Daemon',
                    epilog='')
subparsers = parser.add_subparsers(help='command help', required=True)
parser_ping = subparsers.add_parser('ping', help='ping help')
parser_ping.set_defaults(func=ping)
parser_listen = subparsers.add_parser('listen', help='listen help')
parser_listen.add_argument('fname', type=str, help='fname help')
parser_listen.set_defaults(func=listen)

args = parser.parse_args()
args.func(args)
