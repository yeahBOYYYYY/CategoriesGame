import socket

from command import Command


class Protocol:
    """
    A class that represents the protocol of the server-client communication.
    """

    LENGTH_FIELD_SIZE: int = 4  # the size of the length field in the protocol
    PORT: int = 8820  # the port of the server

    @staticmethod
    def create_msg(cmd: Command) -> bytes:
        """
        Create a message according to the protocol.
        :param cmd: the command to send.
        :returns: the message to send.
        """

        command_name: str = cmd.command.value.encode()
        args_uncoded: list[str] = cmd.args

        # encode the arguments
        args = [args_uncoded[i].encode() for i in range(len(args_uncoded))]

        # create encoded message
        command_bytes: bytes = b" ".join([command_name] + args)

        # add the length of data size & the data size to the data
        data_size = str(len(command_bytes)).encode()
        data_size_length = str(len(data_size)).zfill(Protocol.LENGTH_FIELD_SIZE).encode()
        return data_size_length + data_size + command_bytes

    @staticmethod
    def get_msg(sock: socket.socket) -> tuple[bool, Command | None]:
        """
        Extract message from protocol, without the length field.
        :param sock: active socket to receive from.
        :returns: a bool representing if the data and protocol are valid. And a Command instance or null, depending on the validity.
        """

        length: str = sock.recv(Protocol.LENGTH_FIELD_SIZE).decode()
        if not length.isdigit():
            return False, None

        # read message size and make sure it's an integer
        size: str = sock.recv(int(length)).decode()
        if not size.isdigit():
            return False, None

        # read message and return
        left: int = int(size)
        message: bytes = sock.recv(left)

        try:
            return True, Command(message)
        except:
            return False, None
