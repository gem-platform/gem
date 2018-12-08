"""Abstract endpoint class."""
from abc import ABCMeta, abstractmethod

from gem.core.event import Event


class Endpoint(metaclass=ABCMeta):
    """
    Abstract class for application endpoint.
    """

    def __init__(self):
        """Initializes new instance of the Endpoint class."""
        self.__event = Event()

    @property
    def event(self):
        """Return event."""
        return self.__event

    @abstractmethod
    def open(self):
        """Open endpoint."""
        pass

    @abstractmethod
    def close(self):
        """Close endpoint."""
        pass

    @abstractmethod
    def emit(self, event, data, to=None):
        """Emit event."""
        pass

    @abstractmethod
    def join(self, sid, room):
        pass

    @abstractmethod
    def leave(self, sid, room):
        pass
