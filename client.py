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
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.server_socket.connect((ip_address, port))
        except Exception as e:
            raise InternalException("Please check if a server is running or use a valid ip", e)

    @staticmethod
    def get_command_from_user() -> Command:
        """
        Get a command from the user.
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
        Handle the request from the client
        :param validity: the validity of the command.
        :param cmd: the command to handle.
        :param last_command: the last command that the user have sent to the server.
        :returns: the response command to the client.
        """

        if not validity:
            raise InternalException("Command given isn't valid.")

        try:
            match cmd.command:
                case CommandName.ERROR:
                    return Client.get_command_from_user()
                case CommandName.SUCCESS:
                    # TODO: success
                    print("Success!")
                    return Client.get_command_from_user()
                case CommandName.FAIL:
                    # TODO: fail
                    print("Fail!")
                    return Client.get_command_from_user()
                case _:
                    raise InternalException("Command not meant for server.")
        except Exception as e:  # if there is a problem in Command class, move it upwards
            raise e

    def main(self):
        # the last command that the user have sent to the server.
        sent_command: Command = self.get_command_from_user()
        request = Protocol.create_msg(sent_command)

        self.server_socket.send(request)

        while True:
            validity, cmd = Protocol.get_msg(self.server_socket)

            try:  # handle the response, if not valid will send an exception
                print(f"Received: {cmd.command.value} with args {cmd.args}")
                response_command: Command = self.handle_server_response(validity, cmd, sent_command)
            except:
                response_command: Command = Command(CommandName.ERROR.value)

            # update the last command sent to the server.
            sent_command = response_command

            # create the final message to return to client.
            response = Protocol.create_msg(response_command)
            self.server_socket.send(response)