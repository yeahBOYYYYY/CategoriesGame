import os
import uuid

from Cryptodome.Cipher import AES


class AESCipher:
    """
    AESCipher class to encrypt and decrypt messages of any length using AES algorithm.
    Based on, https://gist.github.com/syedrakib/d71c463fc61852b8d366.
    """

    padding_character: str = "{"
    AES_key_length: int = 16  # AES key length in bytes

    def __init__(self, key: bytes | None = None, nonce: bytes | None = None):
        """
        Constructor for AESCipher class.
        :param key: the key to use for the AES cipher. If None, a random key will be generated.
        :param nonce: the nonce to use for the AES cipher.
        """

        if key is None:
            self.key: bytes = os.urandom(self.AES_key_length)
        else:
            self.key: bytes = key

        if nonce is None:
            self.nonce: bytes = uuid.uuid4().bytes
        else:
            self.nonce: bytes = nonce

    def encrypt_message(self, msg: str) -> bytes:
        """
        Encrypt a message using AES algorithm.
        :param msg: the message to encrypt.
        :return: the encrypted message.
        """

        cipher = AES.new(self.key, AES.MODE_EAX, nonce=self.nonce)
        padded_private_msg = msg + (
                    self.padding_character * ((16 - len(msg)) % 16))  # AES works only on blocks of 16 bytes
        encrypted_msg = cipher.encrypt(padded_private_msg.encode("utf-8"))
        return encrypted_msg

    def decrypt_message(self, msg: bytes) -> str:
        """
        Decrypt a message using AES algorithm.
        :param msg: the message to decrypt.
        :return: the decrypted message.
        """

        cipher = AES.new(self.key, AES.MODE_EAX, nonce=self.nonce)
        decrypted_msg = cipher.decrypt(msg)
        unpadded_private_msg = decrypted_msg.decode().rstrip(self.padding_character)
        return unpadded_private_msg


if __name__ == "__main__":
    private_msg = "This is4אחל51 a private message"
    aes = AESCipher()
    encrypted = aes.encrypt_message(private_msg)
    decrypted = aes.decrypt_message(encrypted)

    print(f"Secret Key: {private_msg} - {len(private_msg)}")
    print(f"Encrypted Msg: {encrypted} - {len(encrypted)}")
    print(f"Decrypted Msg: {decrypted} - {len(decrypted)}")
