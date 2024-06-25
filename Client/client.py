import socket

import rsa

from command import Command, CommandName
from internal_exception import InternalException
from protocol import Protocol
from Client.Gui.window import Window


class Client:
    """
    The client class, responsible for the client side of the application.
    """

    username: str | None = None  # client's username if logged to the server
    score: list[int, int] = [0, 0]  # client's score if logged to the server

    def __init__(self, ip_address: str, port: int = Protocol.PORT):
        """
        Constractor for Client class, creates a socket with parameters given.
        :param ip_address: the ip address of the server.
        :param port: the port of the server. Default is as in the mutual protocol, not a specific case used port.
        """

        print("Connecting to server...")
        print(f"Connecting to {ip_address}:{port}")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.server_socket.connect((ip_address, port))
        except Exception as e:
            raise InternalException("Please check if a server is already running or use a valid ip.", e)

        # generate public and private keys for communication
        self.public_key, self.private_key = rsa.newkeys(Protocol.RSA_KEY_SIZE)

        self.server_public_key: rsa.PublicKey | None = None

    @staticmethod
    def get_command_from_user() -> Command:
        """
        Get a command from the user, used for no GUI.
        :return: the command to send to the server.
        """

        command: Command = Command(CommandName.ERROR.value)  # initialize with error command

        legal_command = False
        while not legal_command:
            try:
                command_str = input("Enter command: ")
                command: Command = Command(command_str)
                legal_command = True
            except:
                print("Invalid command. Please try again.")

        return command

    @staticmethod
    def handle_server_response(validity: bool, cmd: Command, last_command: Command) -> Command:
        """
        Handle the request from the client, used for no GUI.
        Has limited commands available, Login, Signup, Exit, Error.
        :param validity: the validity of the command.
        :param cmd: the command to handle.
        :param last_command: the last command that the user has sent to the server.
        :returns: the response command to the client.
        """

        if not validity:
            raise InternalException("Command given isn't valid.")

        try:
            match cmd.command:
                case CommandName.ERROR:
                    return Client.get_command_from_user()
                case CommandName.SUCCESS:
                    return Client.get_command_from_user()
                case CommandName.FAIL:
                    return Client.get_command_from_user()
                case _:
                    raise InternalException("Command not meant for client.")
        except Exception as e:  # if there is a problem in Command class, move it upwards
            raise e

    def three_way_handshake(self) -> rsa.PublicKey:
        """
        Perform a three-way handshake with the client.
        :return: True if the handshake was successful, False otherwise.
        """

        # get HELLO with public key from server.
        validity, cmd = Protocol.get_msg(self.server_socket)
        if not validity:
            raise InternalException("Command given isn't valid.")
        elif cmd.command != CommandName.HELLO:
            raise InternalException("Command given isn't valid.")

        server_public_key = rsa.PublicKey(int(cmd.args[0]), 65537)

        # send HELLO with public key to server.
        response = Protocol.create_msg(Command(CommandName.HELLO.value, str(self.public_key.n)))
        self.server_socket.send(response)

        # get SUCCESS from server.
        validity, cmd = Protocol.get_msg(self.server_socket)
        if not validity:
            raise InternalException("Command given isn't valid.")
        elif cmd.command != CommandName.SUCCESS:
            raise InternalException("Command given isn't valid.")

        return server_public_key

    def main_user_input(self) -> None:
        """
        Used as the main function of the client when no GUI is needed, responsible for the communication with the server.
        """

        # start communication by exchanging public keys
        try:
            server_public_key: rsa.PublicKey | None = self.three_way_handshake()
        except:
            self.server_socket.close()
            raise InternalException("Handshake failed. Closing connection.")

        # the last command that the user has sent to the server.
        sent_command: Command = self.get_command_from_user()
        request = Protocol.create_msg(sent_command, server_public_key)

        self.server_socket.send(request)

        while True:
            validity, cmd = Protocol.get_msg(self.server_socket, self.private_key)

            try:  # handle the response, if not valid will send an exception
                print(f"Received: {cmd.command.value} with args {cmd.args}")
                response_command: Command = self.handle_server_response(validity, cmd, sent_command)
            except:
                response_command: Command = Command(CommandName.ERROR.value)

            # update the last command sent to the server.
            sent_command = response_command

            # create the final message to return to the client.
            response = Protocol.create_msg(response_command, server_public_key)
            self.server_socket.send(response)

    def main(self):
        """
        Main function of the client with GUI.
        """

        # start communication by exchanging public keys
        try:
            self.server_public_key = self.three_way_handshake()
        except:
            self.server_socket.close()
            raise InternalException("Handshake failed. Closing connection.")

        # create the main GUI window
        window: Window = Window(self)

    def send_and_get(self, cmd: Command) -> tuple[bool, Command]:
        """
        Send a command to the server and get a response.
        :param cmd: the command to send to the server.
        :return: the validity of the command and the command itself.
        """

        sent_command: Command = cmd
        request = Protocol.create_msg(sent_command, self.server_public_key)
        self.server_socket.send(request)
        print("Sent command to server.")

        validity, cmd = Protocol.get_msg(self.server_socket, self.private_key)
        print("Got command from server.")

        return validity, cmd


if __name__ == "__main__":
    client = Client("127.0.0.1")
    client.main_user_input()