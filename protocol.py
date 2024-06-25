import socket
import rsa

from command import Command
from aes_cipher import AESCipher


class Protocol:
    """
    A class that represents the protocol of the server-client communication.
    """

    LENGTH_FIELD_SIZE: int = 4  # the size of the length field in the protocol
    PORT: int = 9960  # the port of the server
    ERROR_LIMIT: int = 10  # limit of sequential errors
    RSA_KEY_SIZE: int = 512  # the size of the RSA key in bits
    TIMEOUT: int = 60*5  # the timeout of the server connection with a client

    @staticmethod
    def create_msg(cmd: Command, public_key: rsa.PublicKey | None = None) -> bytes:
        """
        Create a message according to the protocol.
        :param cmd: the command to send.
        :param public_key: the public key to encrypt the message with, or None if shouldn't be encrypted.
        :returns: the message to send.
        """

        # create the full command with the command name and the arguments
        full_command: str = " ".join([cmd.command.value] + cmd.args)

        # create encoded command
        command_bytes: bytes = full_command.encode()

        # make the message content encrypted with AES
        if public_key is not None:
            aes = AESCipher()
            result_aes: bytes = aes.encrypt_message(full_command)  # encode the message with AES
            command_bytes = result_aes  # send the AES encode key encoded with RSA with the AES encoded message

        # add the length of data size & the data size to the data
        data_size: bytes = str(len(command_bytes)).encode()
        data_size_length: bytes = str(len(data_size)).zfill(Protocol.LENGTH_FIELD_SIZE).encode()

        result: bytes = data_size_length + data_size + command_bytes

        # add the AES key to the message
        if public_key is not None:
            key_rsa: bytes = rsa.encrypt(aes.key, public_key)  # encode the AES key with RSA
            nonce_rsa: bytes = rsa.encrypt(aes.nonce, public_key)  # encode the AES nonce with RSA
            result = key_rsa + nonce_rsa + result

        return result

    @staticmethod
    def get_msg(sock: socket.socket, private_encrypt: rsa.key.PrivateKey | None = None) -> tuple[bool, Command | None]:
        """
        Extract message from protocol, without the length field.
        :param sock: active socket to receive from.
        :param private_encrypt: if the data is encrypted will contain the private RSA key.
        :returns: a bool representing if the data and protocol are valid. And a Command instance or null, depending on the validity.
        """

        try:
            if private_encrypt is not None:
                aes_key_encoded = sock.recv(int(Protocol.RSA_KEY_SIZE / 8))  # convert bit to byte
                aes_nonce_encoded = sock.recv(int(Protocol.RSA_KEY_SIZE / 8))  # uuid is always 16 bytes
                aes_key = rsa.decrypt(aes_key_encoded, private_encrypt)
                aes_nonce = rsa.decrypt(aes_nonce_encoded, private_encrypt)

            # read the length of size header the message
            length: str = sock.recv(Protocol.LENGTH_FIELD_SIZE).decode()
            if not length.isdigit():
                return False, None

            # read message size and make sure it's an integer
            size: str = sock.recv(int(length)).decode()
            if not size.isdigit():
                return False, None

            # read message and return
            left: int = int(size)
            message: bytes | str = sock.recv(left)

            if private_encrypt is not None:
                message = AESCipher(aes_key, aes_nonce).decrypt_message(message)

            return True, Command(message)

        except socket.timeout as e:  # if the socket timed out
            raise e
        except Exception as e:  # if the message is not valid
            return False, None


if __name__ == "__main__":
    public_key, private_key = rsa.newkeys(Protocol.RSA_KEY_SIZE)
    print(len(rsa.encrypt("dgd11g".encode(), public_key)))

    print(type(public_key.n))

    a = Protocol.create_msg(Command("LOGIN user pass"), public_key)
    print(a)
