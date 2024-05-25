class InternalException(Exception):
    def __init__(self, message):
        """
        Constructor for InternalException class.
        :param message: message to print when exception is raised.
        """
        # Call the base class constructor
        super().__init__(message)

        self.message = message

    def __str__(self):
        """
        String representation of the exception.
        :returns: the message of the exception.
        """
        return self.message