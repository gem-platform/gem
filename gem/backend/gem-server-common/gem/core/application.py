"""Abstract class for GEM Platform applications."""
from abc import ABCMeta

from gem.core.endpoints import Endpoints


class Application(metaclass=ABCMeta):
    """
    GEM Application.
    """

    def __init__(self):
        """
        Initializes new instance of the Application class.
        """
        self.__endpoints = Endpoints()

    @property
    def endpoints(self):
        """
        Return list of endpoints.

        Returns:
            list[Endpoint] -- List of endpoints.
        """
        return self.__endpoints

    def run(self):
        """
        Runs application.
        """
        for endpoint in self.__endpoints.all:
            # todo: run in a separate thread
            endpoint.open()
