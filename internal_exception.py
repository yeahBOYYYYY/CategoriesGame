class InternalException(Exception):
    """
    An exception class that is used for internal exceptions.
    """

    debug = False  # debug mode

    def __init__(self, message, e: Exception = None):
        """
        Constructor for InternalException class.
        :param message: message to print when exception is raised.
        """
        # Call the base class constructor
        super().__init__(message)

        self.message = message
        self.real = e

    def __str__(self):
        """
        String representation of the exception.
        :returns: the message of the exception.
        """
        return self.message


def handel_exceptions(ex: Exception) -> None:
    """
    Handle exceptions that occur in the main function.
    :param ex: the exception that occurred.
    """

    if isinstance(ex, InternalException):
        if InternalException.debug:
            print(ex.real)
        else:
            print("\nEXCEPTION: " + str(ex))
    else:
        if InternalException.debug:
            print(ex)
        else:
            print("\nEXCEPTION: An error occurred.")