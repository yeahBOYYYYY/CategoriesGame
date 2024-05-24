import sys

from client import Client
from protocol import Protocol
from server import Server


def decipher_and_start(args: list[str]):
    if args[0] == "client":
        client = Client(args[1], Protocol.PORT)  # client.main()
    elif args[0] == "server":
        server = Server("0.0.0.0", 9960)
        server.main()


if __name__ == "__main__":
    decipher_and_start(sys.argv[1:])
