import socket
import rsa

from command import Command
from internal_exception import InternalException


class Protocol:
    """
    A class that represents the protocol of the server-client communication.
    """

    RSA_KEY_SIZE: int = 1024  # the size of the RSA key
    MESSAGE_LENGTH_BITS = RSA_KEY_SIZE - 88  # the maximum length of the message in bits

    LENGTH_FIELD_SIZE: int = 10  # the size of the length field

    PORT: int = 9960  # the port of the server
    ERROR_LIMIT: int = 10  # limit of sequential errors

    @staticmethod
    def create_msg(cmd: Command, public_encrypt: rsa.key.PublicKey | None = None) -> bytes:
        """
        Create a message according to the protocol.
        :param cmd: the command to send.
        :param public_encrypt: encrypt the data with receiver public RSA key, if no RSA than None.
        :returns: the message to send.
        """

        command_name: bytes = cmd.command.value.encode()
        args_uncoded: list[str] = cmd.args

        # encode the arguments
        args = [args_uncoded[i].encode() for i in range(len(args_uncoded))]

        # create encoded message
        command_bits: bytes = b" ".join([command_name] + args)

        if len(command_bits) > Protocol.MESSAGE_LENGTH_BITS:
            raise InternalException("Message too long to send.")

        command_bits.zfill()

        return data_size_length + data_size + command_bytes

    @staticmethod
    def get_msg(sock: socket.socket, private_encrypt: rsa.key.PrivateKey | None = None) -> tuple[bool, Command | None]:
        """
        Extract message from protocol, without the length field.
        :param sock: active socket to receive from.
        :param private_encrypt: if the data is encrypted will contain the private RSA key, else None.
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
