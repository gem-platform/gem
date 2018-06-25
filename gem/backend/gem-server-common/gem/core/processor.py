"""Commands processor."""

class Processor:
    """Commands processor to manipulate meeting state."""

    def __init__(self):
        """
        Initializes new instance of the Processor class.
        """
        self.__handlers = {}
        self.__context = None

    @property
    def context(self):
        """
        Returns processor execution context.
        :return: User defined object.
        """
        return self.__context

    @context.setter
    def context(self, value):
        """
        Sets processor execution context.
        :param value: User defined object.
        """
        self.__context = value

    def register(self, command, handler):
        """
        Registers handler for specified command.
        :type command: str
        :type handler: callable
        :param command: Command
        :param handler: Handler
        """
        self.__handlers[command] = handler

    def register_handlers(self, handlers):
        """
        Registers a bunch of handlers. Expands to:
        register(handler[0], handler[1]) for each handler.

        Arguments:
            handlers {list[(name, handler)]} -- List of tuple (name, handler)
        """

        for handler in handlers:
            self.register(handler[0], handler[1])

    def exec(self, command, *data):
        """
        Executes command with specified data
        :param command: Command to execute
        :param data: Data to pass to handler
        """
        if command not in self.__handlers:
            raise Exception("No '{}' command registered".format(command))

        return self.__handlers[command](self.__context, *data)
