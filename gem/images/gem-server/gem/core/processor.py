"""Commands processor."""


class Processor:
    """Commands processor to manipulate meeting state."""

    def __init__(self, context):
        """
        Initializes new instance of the Processor class.
        """
        self.__handlers = {}
        self.__context = context

    @property
    def context(self):
        """
        Returns processor execution context.

        Returns:
            obj -- User defined object.
        """
        return self.__context

    def register(self, command, handler):
        """
        Register handler for specified command.

        Arguments:
            command {str} -- Command name.
            handler {func} -- Command handler.
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
        Executes command with specified data.

        Arguments:
            command {str} -- Command to execute.

        Raises:
            Exception -- If command is not registered.

        Returns:
            obj -- Result of execution.
        """
        if command not in self.__handlers:
            raise Exception("No '{}' command registered".format(command))

        return self.__handlers[command](self.__context, *data)
