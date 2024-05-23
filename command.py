from enum import Enum


class Command:
    """
    A class that represents a command in the protocol. It is used to parse the command and its parameters from the socket.
    """

    class CommandName(Enum):
        """
        An enum class that represents the command names in the protocol.
        """

        EXIT = "EXIT"  # exit from the application.
        LOGIN = "LOGIN"  # login to a user.
        LOGOUT = "LOGOUT"  # logout from user.
        # SCORE = "SCORE"  # score of user.
        # GAME_DUAL = "DUAL"  # start a 1v1 game.
        # GAME_PRACTICE = "PRACTICE"  # start a practice game.
        # SUBMIT_ANSWERS = "SUBMIT"  # submits answers in a game.
        # GAME_ENDED = "ENDED"  # the game have ended.

    params_per_command = {  # number of parameters expected for each command
        CommandName.EXIT: 0,
        CommandName.LOGIN: 3,
        CommandName.LOGOUT: 2,
    }

    def __init__(self, data: str | bytes):
        if type(data) == bytes:
            data = data.decode()
        words = self.extract_words(data)

        if words[0] not in Command.CommandName:
            raise Exception("Command not defined in the protocol")
        self.command = Command.CommandName(words[0])

        if len(words) - 1 != Command.params_per_command[self.command]:
            raise Exception("Invalid number of parameters for the command")
        self.args = words[1:]

    @staticmethod
    def extract_words(data: str) -> list[str]:
        """
        Extract the command and parameters from a valid request. For example, for 'DIR path' the returned value is ['DIR', path].
        :param data: the command and parameters passed in the socket.
        :returns: a list of the command and its parameters.
        """

        data = data.strip()  # trim whitespaces at the ends
        return data.split(" ")
