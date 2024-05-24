import socket

from command import Command, CommandName
from protocol import Protocol


class Server:
    def __init__(self, ip_address: str, port: int = Protocol.PORT):
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

    def main(self):
        client_socket, client_address = self.ServerSocket.accept()

        # handle requests until user asks to exit
        while True:
            validity, cmd = Protocol.get_msg(client_socket)

            try:  # handle the request, if not valid will raise an exception
                response = self.handle_client_request(validity, cmd)
                print(f"Received: {cmd.command.value} with args {cmd.args}")
            except:
                response = Protocol.create_msg(Command(CommandName.ERROR.value))

            client_socket.send(response)
            if cmd == CommandName.EXIT:
                break

        self.ServerSocket.close()
        client_socket.close()
        print("Closing connection...")

    def handle_client_request(self, validity: bool, cmd: Command) -> bytes:
        """
        Handle the request from the client
        :param validity: the validity of the command.
        :param cmd: the command to handle.
        :returns: the response to the client.
        """
        pass
