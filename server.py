import socket
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
            command = ""
            valid_protocol, cmd = Protocol.get_msg(client_socket)

            # if valid_protocol:
            #     # check if params are good, e.g. correct number of params, file name exists
            #     # valid_cmd, command, params = self.check_client_request(cmd.decode())
            #     # if valid_cmd:
            #     #     response = self.handle_client_request(command, params)
            #     #
            #     #     if command == Protocol.SEND_PHOTO:
            #     #         image_file = open(self.PHOTO_PATH, "rb")
            #     #         response = image_file.read()
            #     # else:
            #     #     response = "Not valid parameters"
            #     pass
            # else:
            #     response = "Packet not according to protocol"
            #     client_socket.recv(1024)    # clean garbage from socket
            # response = "Packet not according to protocol"
            # response = Protocol.create_msg(response)
            # client_socket.send(response)

            if command == Protocol.EXIT:
                break

        self.ServerSocket.close()
        client_socket.close()
        print("Closing connection...")