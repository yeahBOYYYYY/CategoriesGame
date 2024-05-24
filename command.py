from enum import Enum


class CommandName(Enum):
    """
    An enum class that represents the command names in the protocol.
    """

    ERROR: str = "ERROR"  # error message.
    EXIT: str = "EXIT"  # exit from the application.
    LOGIN: str = "LOGIN"  # login to a user.
    LOGOUT: str = "LOGOUT"  # logout from user.
    SIGNUP: str = "SIGNUP"  # sign up a new user.  # SCORE = "SCORE"  # score of user.  # GAME_DUAL = "DUAL"  # start  # a 1v1 game.  # GAME_PRACTICE = "PRACTICE"  # start a practice game.  # SUBMIT_ANSWERS = "SUBMIT"  # submits  # answers in a game.  # GAME_ENDED = "ENDED"  # the game have ended.


class Command:
    """
    A class that represents a command in the protocol. It is used to parse the command and its parameters from the socket.
    """

    params_per_command: dict[CommandName, int] = {  # number of parameters expected for each command
        CommandName.ERROR: 0, CommandName.EXIT: 0, CommandName.LOGIN: 2, CommandName.SIGNUP: 3, CommandName.LOGOUT: 0, }

    def __init__(self, data: str | bytes):
        if isinstance(data, bytes):
            data: str = data.decode()
        words: list[str] = self.extract_words(data)

        if words[0] not in CommandName:
            raise Exception("Command not defined in the protocol")
        self.command: CommandName = CommandName(words[0])

        if len(words) - 1 != Command.params_per_command[self.command]:
            raise Exception("Invalid number of parameters for the command")
        self.args: list[str] = words[1:]

    @staticmethod
    def extract_words(data: str) -> list[str]:
        """
        Extract the command and parameters from a valid request. For example, for 'DIR path' the returned value is ['DIR', path].
        :param data: the command and parameters passed in the socket.
        :returns: a list of the command and its parameters.
        """

        data: str = data.strip()  # trim whitespaces at the ends
        return data.split(" ")
