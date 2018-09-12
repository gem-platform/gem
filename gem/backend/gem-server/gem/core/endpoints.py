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

        Returns:
            list[Endpoint] -- List of all events.
        """
        # todo: return readonly
        return self.__endpoints

    @property
    def event(self):
        """
        Event of endpoint.

        Returns:
            Event -- Event.
        """
        return self.__event

    def add(self, endpoint):
        """
        Add endpoint to list.

        Arguments:
            endpoint {Endpoint} -- Endpoint to add.
        """
        self.__endpoints.append(endpoint)
        endpoint.event.subscribe(self.__on_endpoint_event)

    def __on_endpoint_event(self, event, *data):
        """
        On endpoint event.

        Arguments:
            event {str} -- Event

        Returns:
            obj -- Result
        """
        return self.__event.notify(event, *data)
