"""Meeting server application class."""
from logging import getLogger

from gms.app.active_meetings import ActiveMeetings
from gms.net import SocketIoEndpoint


class MeetingServerApplication:
    """GEM Meeting Server application."""

    def __init__(self, host: str, port: int):
        """
        Initialize a new instance of the MeetingServerApplication class.

        Arguments:
            host {str} -- Host to listen on
            port {int} -- Port to listen on
        """
        # get a logger
        self.__log = getLogger("root")

        # create socket io endpoint to listen on
        self.__endpoint = SocketIoEndpoint(host, port)
        self.__endpoint.event.subscribe(self.__on_endpoint_event)

        # active meetings manager
        self.__active_meetings = ActiveMeetings(self.__endpoint)

    def __on_endpoint_event(self, event: str, *data):
        """
        On endpoint event.

        Arguments:
            event {str} -- Name of the event.
            data {dict} -- Data passed.

        Returns:
            obj -- Result of the event.
        """
        try:
            return self.__active_meetings.command(event, *data)
        except Exception as exc:  # pylint: disable=broad-except
            message = "Error while processing '{}' event: {}".format(event, str(exc))
            self.__log.error(message)
            self.__log.exception(exc)
            return {"success": False, "message": message}

    def start(self):
        """Start application."""
        self.__endpoint.open()

    def stop(self):
        """Stop application"""
        self.__endpoint.close()
