import socket
from command import Command


class Protocol:
    LENGTH_FIELD_SIZE = 4
    PORT = 8820

    @staticmethod
    def create_msg(command: str) -> bytes:
        #TODO: Implement this method
        """
        Create a valid protocol message, with length field.
        :param command: the command to send in the socket.
        :returns: encoded data by the protocol standards.
        """
        if type(command) == str:
            command = command.encode()

        # add the length of data size & the data size to the data
        data_size = str(len(command)).encode()
        data_size_length = str(len(data_size)).zfill(Protocol.LENGTH_FIELD_SIZE).encode()
        return data_size_length + data_size + command

    @staticmethod
    def get_msg(sock: socket.socket) -> tuple[bool, Command | None]:
        """
        Extract message from protocol, without the length field.
        :param sock: active socket to receive from.
        :returns: a bool representing if the data and protocol are valid. And a Command instance or null, depending on the validity.
        """

        length = sock.recv(Protocol.LENGTH_FIELD_SIZE).decode()
        if not length.isdigit():
            return False, None

        # read message size and make sure it's an integer
        size = sock.recv(int(length)).decode()
        if not size.isdigit():
            return False, None

        # read message and return
        left = int(size)
        message = sock.recv(left)

        try:
            return True, Command(message)
        except:
            return False, None
