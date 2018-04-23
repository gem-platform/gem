from gem.core.event import Event


class Endpoints:
    """
    Application endpoints.
    """

    def __init__(self):
        """
        Initializes new instance if the endpoint class.
        """
        self.__endpoints = []
        self.__event = Event()

    @property
    def all(self):
        """
        Returns list of all endpoints.
        :rtype: list[Endpoint]
        :return: List of endpoints.
        """
        # todo: return readonly
        return self.__endpoints

    @property
    def event(self):
        """
        On event of endpoint.
        :rtype: Event
        :return: Event
        """
        return self.__event

    def add(self, endpoint):
        """
        Adds endpoint.
        :type endpoint: Endpoint
        :param endpoint: Endpoint to add.
        """
        self.__endpoints.append(endpoint)
        endpoint.event.subscribe(self.__on_endpoint_event)

    def __on_endpoint_event(self, event, *data):
        """
        On endpoint event.
        :param event: Name of event.
        :param data: Data of event.
        :return: Result of event's handler.
        """
        return self.__event.notify(event, *data)
