import socket
import sys
import threading

import select

import internal_exception
from command import Command, CommandName
from internal_exception import InternalException
from protocol import Protocol
from Database.database import Database


class Server:
    def __init__(self, ip_address: str, port: int = Protocol.PORT):
        """
        Constractor for Client class, creates a socket with parameters given.
        :param ip_address: the ip address of the server.
        :param port: the port of the server. Default is as in the mutual protocol, not a specific case used port.
        """

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # allow other sockets to bind to this port
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((ip_address, port))
        except Exception as e:
            raise InternalException("Please check if a server is running or use a valid ip", e)

        self.server_socket.listen()
        print("Server is up and running!")
        print(f"Listening on {ip_address}:{port}")

        # threads list to keep track of all clients
        self.threads: list[threading.Thread] = []

        # create a database object
        self.database: Database = Database()

    def login_request(self, username: str, password: str) -> Command:
        """
        Check if the user login info are valid in the database.
        :param username: the username of the client.
        :param password: the password of the client.
        :returns: the response command to the client.
        """

        if self.database.is_valid_user(username, password):
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

    def handle_client(self, client_socket: socket.socket, client_address: tuple[str, int]) -> None:
        """
        Handle the client.
        :param client_socket: the socket of the client.
        :param client_address: the address of the client.
        """

        print(f"Handling connection with {client_address}")

        # if the client sends an error message, we need to remember what we sent last
        prev_response_command: Command = Command(CommandName.ERROR.value)

        # sequentially error counter
        errors: int = 0

        # handle requests until user asks to exit
        while True:
            validity, cmd = Protocol.get_msg(client_socket)

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
            client_socket.send(response)

            if cmd.command == CommandName.EXIT:
                break

        client_socket.close()
        print(f"Closing connection with {client_address}")

    def main(self):
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection from {client_address}")

                # start a thread for the client
                try:
                    t = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                    t.start()
                    self.threads.append(t)
                except InternalException as e:
                    internal_exception.handel_exceptions(e)
                    client_socket.close()

        except Exception as e:
            raise InternalException("Server has stopped working due to an error.", e)
        finally:
            print("Server is shutting down...")
            for thread in self.threads:
                thread.join()
            self.server_socket.close()
