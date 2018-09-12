"""Event class."""


class Event:
    """Event."""

    def __init__(self):
        """
        Initializes new instance of the Event class.
        """
        self.handlers = []

    def subscribe(self, handler):
        """
        Subscribe for the event.

        Arguments:
            handler {func} -- Handler.

        Raises:
            Exception -- If handler already registered.
        """
        if handler not in self.handlers:
            self.handlers.append(handler)
        else:
            raise Exception("Already subscribed on specified handler")

    def unsubscribe(self, handler):
        """
        Unsubscribe from the event.

        Arguments:
            handler {func} -- Handler.

        Raises:
            Exception -- If handler not registered.
        """
        if handler in self.handlers:
            self.handlers.remove(handler)
        else:
            raise Exception("Not subscribed on specified handler")

    def notify(self, *args):
        """
        Notify subscribers
        
        Returns:
            obj -- Result.
        """
        result = None
        for handler in self.handlers:
            # todo: if multiple handlers registered?
            result = handler(*args)

        return result
