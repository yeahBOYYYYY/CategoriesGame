import socket


class Protocol:
    EXIT = "EXIT"               # exit from the application.
    LOGIN = "LOGIN"             # login to a user.
    LOGOUT = "LOGOUT"           # logout from user.
    SCORE = "SCORE"             # score of user.
    GAME_DUAL = "DUAL"          # start a 1v1 game.
    GAME_PRACTICE = "PRACTICE"  # start a practice game.
    SUBMIT_ANSWERS = "SUBMIT"   # submits answers in a game.
    GAME_ENDED = "ENDED"        # the game have ended.

    LENGTH_FIELD_SIZE = 4
    PORT = 8820

    NO_PARAM_CMD = {EXIT, LOGOUT, SCORE, GAME_DUAL, GAME_PRACTICE}
    ONE_PARAM_CMD = {GAME_ENDED}
    TWO_PARAM_CMD = {LOGIN}
    FIVE_PARAM_CMD = {SUBMIT_ANSWERS}

    @staticmethod
    def extract_cmd_and_params(data: str) -> tuple[str, list[str]]:
        """
        Extract the command and parameters from a valid request. For example, for 'DIR path' the returned value is 'DIR', [path].
        :param data: the command and parameters passed in the socket.
        """

        data = data.strip()  # trim whitespaces at the ends
        space_index = data.find(" ")

        if space_index == -1:   # command doesn't have a parameter passed
            return data, []

        params = data[space_index + 1:].split(" ")  # params are the rest of the data
        return data[:space_index], params

    @staticmethod
    def check_cmd(command: str) -> bool:
        #@TODO
        """
        Check if the command is defined in the protocol, including all parameters.
        :param command: the command to send in the socket.
        :returns: true if command is legit, else false.
        """

        command = command.strip()     # trim whitespaces at the ends

        space_index = command.find(" ")
        if space_index == -1:   # command is "TAKE_SCREENSHOT"/"SEND_PHOTO"/"EXIT"
            return command in Protocol.NO_PARAM_CMD

        cmd, remaining = command[:space_index], command[space_index + 1:]
        if cmd in Protocol.ONE_PARAM_CMD:   # commands that require one parameter
            return len(remaining) != 0

        if cmd in Protocol.TWO_PARAM_CMD:   # only COPY, requires two parameters
            space_index2 = remaining.strip().find(" ")
            return space_index2 != -1

        return False    # command not defined

    @staticmethod
    def create_msg(command: str) -> bytes:
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
    def get_msg(sock: socket.socket) -> tuple[bool, str]:
        """
        Extract message from protocol, without the length field.
        :param sock: active socket to receive from.
        :returns: a bool representing if the data and protocol are valid. And a string representing the data, if not valid will return False, "Error".
        """

        # read message size length and make sure it's an integer
        response = b""
        while True:
            chunk = sock.recv(4096)
            response = response + chunk
            if len(chunk) < 4096:  # No more data received, quitting
                break
        header_data, _, body = response.partition(b'\r\n\r\n')
        print(header_data.decode())

        # print(sock.recv(1024).decode())
        return

        length = sock.recv(Protocol.LENGTH_FIELD_SIZE).decode()
        if not length.isdigit():
            return False, "Error"

        # read message size and make sure it's an integer
        size = sock.recv(int(length)).decode()
        if not size.isdigit():
            return False, "Error"

        # read message and return
        left = int(size)
        message = sock.recv(left)
        return True, body
