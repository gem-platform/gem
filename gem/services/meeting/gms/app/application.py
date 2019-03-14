"""Meeting server application class."""
from logging import getLogger

from gms.app.active_meetings import ActiveMeetings
from gms.net import SocketIoEndpoint


class MeetingServerApplication:
    """GEM Meeting Server application."""

    def __init__(self, host, port):
        """Initialize new instance of the MeetingServerApplication class."""
        super().__init__()

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
            # add all sockets to "connected" room to be
            # able to send all connected sockets
            if event == "connect":
                self.__endpoint.join(data[0], "connected")

            return self.__active_meetings.command(event, *data)
        except Exception as exc:
            message = "Error while processing '{}' event: {}".format(event, str(exc))
            self.__log.error(message)
            self.__log.exception(exc)
            return {"success": False, "message": message}

    def run(self):
        """Run application."""
        self.__endpoint.open()
