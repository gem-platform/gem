from abc import ABCMeta

from gem.core.endpoints import Endpoints
from gem.core.processor import Processor


class Application(metaclass=ABCMeta):
    """
    GEM Application.
    """

    def __init__(self):
        """
        Initializes new instance of the Application class.
        """
        self.__processor = Processor()
        self.__endpoints = Endpoints()
        self.__endpoints.event.subscribe(self.__on_endpoint_event)

    @property
    def processor(self):
        """
        Returns commands processor.
        :rtype: Processor
        :return: Processor.
        """
        return self.__processor

    @property
    def endpoints(self):
        """
        Returns endpoints of the application.
        :rtype: Endpoints
        :return: Endpoints.
        """
        return self.__endpoints

    def run(self):
        """
        Runs application.
        """
        for endpoint in self.__endpoints.all:
            # todo: run in thread
            endpoint.open()

    def __on_endpoint_event(self, event, *data):
        """
        On endpoint event.
        :param event: Event name.
        :param data: Event data.
        :return: Execution result.
        """
        return self.__processor.exec(event, *data)
