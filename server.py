import socket
from protocol import Protocol


class Server:
    def __init__(self, ip_address: str, port: str = Protocol.PORT):
        """
        Constractor for Client class, creates a socket with parameters given.
        :param ip_address: the ip address of the server.
        :param port: the port of the server. Default is as in the mutual protocol, not a specific case used port.
        """
        self.ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.ServerSocket.bind((ip_address, port))
        except:
            raise Exception("Please check if a server is running or use a valid ip")

        self.ServerSocket.listen()
        print("Server is up and running!")