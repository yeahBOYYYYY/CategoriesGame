import sys

from client import Client
from internal_exception import InternalException
from protocol import Protocol
from server import Server


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

def handel_exceptions(ex: Exception, debug: bool) -> None:
    """
    Handle exceptions that occur in the main function.
    :param ex: the exception that occurred.
    :param debug: if the debug mode is on.
    """
    if debug:
        print(ex)
    else:
        if isinstance(ex, InternalException):
            print("\nEXCEPTION:" + str(ex))
        else:
            print("\nEXCEPTION: An error occurred")

def main(args: list[str]):
    debug = False
    try:
        if args[0] == "-d":  # set debug mode
            debug = True
            args = args[1:]
        else:
            sys.tracebacklimit = 0  # make it not show tree of exceptions

        if (args[0] == "client") and (len(args) == 2):  # client mode
            start_client(args[1])
        elif (args[0] == "server") and (len(args) == 1):  # server mode
            start_server()
        else:
            print(args)
            raise InternalException("Invalid arguments")

    except Exception as ex:
        handel_exceptions(ex, debug)


if __name__ == "__main__":
    main(sys.argv[1:])
