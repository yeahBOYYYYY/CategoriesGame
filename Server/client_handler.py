import socket

from Server.Database.database import Database
from command import Command, CommandName
from internal_exception import InternalException
from protocol import Protocol


class ClientHandler:
    """
    The client handler class, handles the server client communication side of the server.
    """

    def __init__(self, client_socket: socket.socket, client_address: tuple[str, int], database: Database):
        """
        Constractor for ClientHandler class, initializes the client values.
        :param client_socket: the socket of the client.
        :param client_address: the address of the client.
        """

        print(f"Handling connection with {client_address}")

        self.client_socket = client_socket
        self.client_address = client_address
        self.database = database

        self.username: str | None = None

    def login_request(self, username: str, password: str) -> Command:
        """
        Check if the user login info are valid in the database.
        :param username: the username of the client.
        :param password: the password of the client.
        :returns: the response command to the client.
        """

        if self.database.is_valid_user(username, password):
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

        if self.database.add_user(username, password, email):
            self.username = username
            return Command(CommandName.SUCCESS.value)
        return Command(CommandName.FAIL.value)

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
                case _:
                    raise InternalException("Command not meant for server.")
        except Exception as e:  # if there is a problem in Command class, move it upwards
            raise e

    def handle_client(self) -> None:
        """
        Handles the sending and receiving from the client.
        """

        # if the client sends an error message, we need to remember what we sent last
        prev_response_command: Command = Command(CommandName.ERROR.value)

        # sequentially error counter
        errors: int = 0

        # handle requests until user asks to exit
        while True:
            validity, cmd = Protocol.get_msg(self.client_socket)

            try:  # handle the request, if not valid will send an exception
                response_command: Command = self.handle_request(validity, cmd, prev_response_command)
                print(f"Received: {cmd.command.value} with args {cmd.args}")
                print(f"Responding with: {response_command.command.value}")
            except:
                response_command: Command = Command(CommandName.ERROR.value)

            # increment number of consecutive errors or reset it
            if prev_response_command == response_command:
                errors += 1
            else:
                errors = 0

            # if a lot of errors sequentially then something went wrong, terminating connection
            if errors >= Protocol.ERROR_LIMIT:
                break

            # renew the prev command to be the last one
            prev_response_command = response_command

            # create the final message to return to client.
            response = Protocol.create_msg(response_command)
            self.client_socket.send(response)

            if cmd.command == CommandName.EXIT:
                break

        self.client_socket.close()
        print(f"Closing connection with {self.client_address}")
