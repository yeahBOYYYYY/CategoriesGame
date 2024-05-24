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

    @staticmethod
    def handle_client_request(validity: bool, cmd: Command, prev_cmd: Command) -> Command:
        """
        Handle the request from the client
        :param validity: the validity of the command.
        :param cmd: the command to handle.
        :param prev_cmd: the last command sent from server.
        :returns: the response command to the client.
        """

        if not validity:
            raise Exception("Command given isn't valid.")

        try:
            match cmd.command:
                case CommandName.ERROR:
                    return prev_cmd
                case CommandName.EXIT:
                    return Command(CommandName.SUCCESS.value)
                case CommandName.LOGIN:
                    # TODO: login
                    pass
                case CommandName.SIGNUP:
                    # TODO: signup
                    pass
                case _:
                    raise Exception("Command not meant for server.")
        except Exception as e:  # if there is a problem in Command class, move it upwards
            raise e

    def main(self):
        client_socket, client_address = self.ServerSocket.accept()

        # if the client sends an error message, we need to remember what we sent last
        prev_response_command: Command = Command(CommandName.ERROR.value)

        # sequentially error counter, using array for mutability
        errors = [0]

        # handle requests until user asks to exit
        while True:
            validity, cmd = Protocol.get_msg(client_socket)

            try:  # handle the request, if not valid will raise an exception
                response_command: Command = self.handle_client_request(validity, cmd, prev_response_command)
                print(f"Received: {cmd.command.value} with args {cmd.args}")
            except:
                response_command: Command = Command(CommandName.ERROR.value)

            # increment number of consecutive errors or reset it
            if prev_response_command == response_command:
                errors[0] += 1
            else:
                errors[0] = 0

            # if a lot of errors sequentially then something went wrong, terminating connection
            if errors[0] >= Protocol.ERROR_LIMIT:
                break

            # renew the prev command to be the last one
            prev_response_command = response_command

            # create the final message to return to client.
            response = Protocol.create_msg(response_command)
            client_socket.send(response)

            if cmd == CommandName.EXIT:
                break

        self.ServerSocket.close()
        client_socket.close()
        print("Closing connection...")
