from __future__ import annotations
import socket
import rsa

from Server.Database.database import Database
from command import Command, CommandName
import internal_exception
from internal_exception import InternalException
from protocol import Protocol


class ClientHandler:
    """
    The client handler class, handles the server client communication side of the server.
    """

    def __init__(self, client_socket: socket.socket, client_address: tuple[str, int], server: "Server.server.Server"):
        """
        Constractor for ClientHandler class, initializes the client values.
        :param client_socket: the socket of the client.
        :param client_address: the address of the client.
        :param server: the parent server object.
        """

        print(f"Handling connection with {client_address}")

        self.client_socket = client_socket
        self.client_address = client_address
        self.server = server

        self.username: str | None = None

    def login_request(self, username: str, password: str) -> Command:
        """
        Check if the user login info is valid in the database.
        :param username: the username of the client.
        :param password: the password of the client.
        :returns: the response command to the client.
        """

        if self.server.database.is_valid_user(username, password):
            self.username = username
            return Command(CommandName.SUCCESS.value)
        return Command(CommandName.FAIL.value)

    def signup_request(self, username: str, password: str, email: str) -> Command:
        """
        Check if the user login info are valid in the database, if they are add them to the database.
        :param username: the username of the client.
        :param password: the password of the client.
        :param email: the email of the client.
        :returns: the response command to the client.
        """

        if self.server.database.add_user(username, password, email):
            self.username = username
            return Command(CommandName.SUCCESS.value)
        return Command(CommandName.FAIL.value)

    def info_request(self) -> Command:
        """
        Get the info of the user.
        :returns: the response command to the client.
        """

        if self.username is None:
            return Command(CommandName.FAIL.value)
        else:
            user_mail = self.server.database.get_mail(self.username)
            user_score = self.server.database.get_score(self.username)
        return Command(CommandName.INFO_RESPONSE.value, self.username, user_mail, user_score)

    def handle_request(self, validity: bool, cmd: Command, prev_cmd: Command) -> Command:
        """
        Handles the request from the client.
        :param validity: the validity of the command.
        :param cmd: the command to handle.
        :param prev_cmd: the last command sent from server.
        :returns: the response command to the client.
        """

        if not validity:
            raise InternalException("Command given isn't valid.")

        try:
            match cmd.command:
                case CommandName.ERROR:
                    return prev_cmd
                case CommandName.EXIT:
                    return Command(CommandName.SUCCESS.value)
                case CommandName.LOGIN:
                    return self.login_request(*cmd.args)
                case CommandName.SIGNUP:
                    return self.signup_request(*cmd.args)
                case CommandName.INFO_REQUEST:
                    return self.info_request()
                case _:
                    raise InternalException("Command not meant for server.")
        except Exception as e:  # if there is a problem in Command class, move it upwards
            raise e

    def three_way_handshake(self) -> rsa.PublicKey:
        """
        Perform a three-way handshake with the client.
        :return: True if the handshake was successful, False otherwise.
        """
        
        # send HELLO with public key to client.
        response = Protocol.create_msg(Command(CommandName.HELLO.value, str(self.server.public_key.n)))
        self.client_socket.send(response)

        # get HELLO with public key from client.
        validity, cmd = Protocol.get_msg(self.client_socket)
        if not validity:
            raise InternalException("Command given isn't valid.")
        elif cmd.command != CommandName.HELLO:
            raise InternalException("Command given isn't valid.")

        client_public_key = rsa.PublicKey(int(cmd.args[0]), 65537)

        # send SUCCESS to client.
        response = Protocol.create_msg(Command(CommandName.SUCCESS.value))
        self.client_socket.send(response)

        return client_public_key


    def handle_client(self) -> None:
        """
        Handles the sending and receiving from the client.
        """

        # start communication by exchanging public keys
        try:
            client_public_key: rsa.PublicKey | None = self.three_way_handshake()
        except:
            self.client_socket.close()
            print(f"Closing connection with {self.client_address}")
            return

        # if the client sends an error message, we need to remember what we sent last
        prev_response_command: Command = Command(CommandName.ERROR.value)

        # sequentially error counter
        errors: int = 0

        # handle requests until user asks to exit
        while True:
            validity, cmd = Protocol.get_msg(self.client_socket, self.server.private_key)

            try:  # handle the request, if not valid will send an exception
                response_command: Command = self.handle_request(validity, cmd, prev_response_command)
                print(f"Received: {cmd.command.value} with args {cmd.args}")
                print(f"Responding with: {response_command.command.value}")
            except:
                response_command: Command = Command(CommandName.ERROR.value)

            # increment the number of consecutive errors or reset it
            if prev_response_command == response_command:
                errors += 1
            else:
                errors = 0

            # if a lot of errors sequentially, then something went wrong, terminating the connection
            if errors >= Protocol.ERROR_LIMIT:
                break

            # renew the prev command to be the last one
            prev_response_command = response_command

            # create the final message to return to the client.
            response = Protocol.create_msg(response_command, client_public_key)
            try:
                self.client_socket.send(response)
            except Exception as e:
                internal_exception.handel_exceptions(e)

            if (cmd is not None) and (cmd.command == CommandName.EXIT):
                break

        self.client_socket.close()
        print(f"Closing connection with {self.client_address}")
