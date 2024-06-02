import socket
import threading

import internal_exception
from Server.client_handler import ClientHandler
from internal_exception import InternalException
from protocol import Protocol
from Server.Database.database import Database


class Server:
    """
    The server class, handles the server connections side of the application.
    """

    def __init__(self, ip_address: str, port: int = Protocol.PORT):
        """
        Constractor for Server class, creates a socket with parameters given.
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
        self.users: list[tuple[ClientHandler, threading.Thread]] = []

        # create a database object
        self.database: Database = Database()

    def stop_server(self):
        """
        Method to stop the server.
        """

        print("Server is shutting down...")
        for _, thread in self.users:
            thread.join()
        self.server_socket.close()

    def listen_for_exit(self):
        """
        Listen for user input to stop the server.
        """

        while True:
            user_input = input()
            if user_input == "EXIT":
                self.stop_server()

    def main(self):
        """
        The main function of the server, handles the server connections and threads.
        """

        try:
            # Start a thread that listens for user input to stop the server
            stop_thread = threading.Thread(target=self.listen_for_exit, daemon=True)
            stop_thread.start()

            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection from {client_address}")

                # start a thread for the client
                try:
                    user = ClientHandler(client_socket, client_address, self.database)
                    t = threading.Thread(target=user.handle_client)
                    t.start()
                    self.users.append((user, t))
                except InternalException as e:
                    internal_exception.handel_exceptions(e)
                    client_socket.close()

        except Exception as e:
            raise InternalException("Server has stopped working due to an error.", e)
        finally:
            self.stop_server()
