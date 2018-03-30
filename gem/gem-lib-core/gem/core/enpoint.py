from abc import ABCMeta, abstractmethod

from gem.core.event import Event


class Endpoint(metaclass=ABCMeta):
    def __init__(self):
        self.__event = Event()

    @property
    def event(self):
        return self.__event

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def emit(self, event, data, to=None):
        pass
