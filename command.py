from enum import Enum

from internal_exception import InternalException


class CommandName(Enum):
    """
    An enum class that represents the command names in the protocol.
    """

    ERROR: str = "ERROR"  # error message.
    HELLO: str = "HELLO"  # hello message.
    EXIT: str = "EXIT"  # exit from the application.
    SUCCESS: str = "SUCCESS"  # if command needs conformation
    FAIL: str = "FAIL"  # if command need conformation.

    LOGIN: str = "LOGIN"  # login to a user.
    SIGNUP: str = "SIGNUP"  # sign up a new user.

    INFO_REQUEST: str = "REQIN"  # request for information.
    INFO_RESPONSE: str = "RESIN"  # response for information.

    WAITING: str = "WAITING"  # waiting for a game.
    MATCH: str = "MATCH"  # match with another player.
    ANSWERS: str = "ANSWERS"  # answers to the questions.


class Command:
    """
    A class that represents a command in the protocol. It is used to parse the command and its parameters from the socket.
    """

    params_per_command: dict[CommandName, int] = {  # number of parameters expected for each command
        CommandName.ERROR: 0,
        CommandName.HELLO: 1,
        CommandName.EXIT: 0,
        CommandName.SUCCESS: 0,
        CommandName.FAIL: 0,
        CommandName.LOGIN: 2,
        CommandName.SIGNUP: 3,
        CommandName.INFO_REQUEST: 0,
        CommandName.INFO_RESPONSE: 2,
        CommandName.WAITING: 0,
        CommandName.MATCH: 2
    }

    def __init__(self, *args: str | bytes | CommandName):
        """
        Constructor for Command class, calls other 'constructors'.
        :param args: the command and parameters passed in the socket.
        """

        if len(args) == 1:
            self.__init_one(args[0])
        else:
            # convert bytes to string if needed in the list of arguments
            args_str: list[str] = []
            for i in range(len(args)):
                if isinstance(args[i], bytes):
                    args_str.append(args[i].decode())
                else:
                    args_str.append(args[i])

            # call the constructor with the joined string arguments
            self.__init_one(" ".join(args))

    def __init_one(self, data: str | bytes):
        """
        Constructor for Command class.
        :param data: the command and parameters passed in the socket.
        """

        if isinstance(data, bytes):  # if the data is bytes, decode it
            data: str = data.decode()
        words: list[str] = self.extract_words(data)  # extract the command and parameters

        if words[0] not in CommandName:  # check if the command is defined in the protocol
            raise InternalException("Command not defined in the protocol")
        self.command: CommandName = CommandName(words[0])

        if len(words) - 1 != Command.params_per_command[self.command]:  # check if the number of parameters is valid
            raise InternalException("Invalid number of parameters for the command")
        self.args: list[str] = words[1:]

    def __str__(self) -> str:
        return f"{self.command.value} {' '.join(self.args)}"

    def __eq__(self, other):
        return (self.command == other.command) and (self.args == other.args)

    @staticmethod
    def extract_words(data: str) -> list[str]:
        """
        Extract the command and parameters from a valid request. For example, for 'DIR path' the returned value is ['DIR', path].
        :param data: the command and parameters passed in the socket.
        :returns: a list of the command and its parameters.
        """

        data: str = data.strip()  # trim whitespaces at the ends
        return data.split(" ")
