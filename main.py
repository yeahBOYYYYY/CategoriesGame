import sys

import internal_exception
from Client.client import Client
from Server.server import Server
from internal_exception import InternalException
from protocol import Protocol


def start_client(ip: str) -> None:  # python main.py client 127.0.0.1
    """
    Start the client with the given ip.
    :param ip: the ip to connect to.
    """

    client = Client(ip, Protocol.PORT)
    client.main()


def start_server() -> None:  # python main.py server
    """
    Start the server.
    """

    server = Server("0.0.0.0", Protocol.PORT)
    server.main()


def main(args: list[str]):
    try:
        if args[0] == "-d":  # set debug mode
            InternalException.debug = True
            args = args[1:]
        else:
            sys.tracebacklimit = 0  # make it not show tree of exceptions

        if (args[0] == "client") and (len(args) == 2):  # client mode
            start_client(args[1])
        elif (args[0] == "server") and (len(args) == 1):  # server mode
            start_server()
        else:
            raise InternalException("Invalid arguments.")

    except Exception as ex:
        internal_exception.handel_exceptions(ex)


if __name__ == "__main__":
    main(sys.argv[1:])
