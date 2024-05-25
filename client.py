import socket

from command import Command, CommandName
from internal_exception import InternalException
from protocol import Protocol


class Client:
    def __init__(self, ip_address: str, port: int = Protocol.PORT):
        """
        Constractor for Client class, creates a socket with parameters given.
        :param ip_address: the ip address of the server.
        :param port: the port of the server. Default is as in the mutual protocol, not a specific case used port.
        """

        print("Connecting to server...")
        print(f"Connecting to {ip_address}:{port}")
        self.ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.ServerSocket.connect((ip_address, port))
        except:
            raise InternalException("Please check if a server is running or use a valid ip")

    def send_command(self, command: Command):
        """
        Sends a command to the server.
        :param command: The command to send.
        """

        self.ServerSocket.send(Protocol.create_msg(command))

    def receive_response(self):
        """
        Receives a response from the server.
        :return: The response from the server.
        """

        response = Protocol.get_msg(self.ServerSocket)
        return response

    def main(self):
        command = Command("LOGIN user password")
        self.send_command(command)
        valid, response = self.receive_response()
        print(f"Received: {response}")
        self.ServerSocket.close()