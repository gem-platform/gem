"""Meeting server application class."""
from logging import getLogger

from gms.app.active_meetings import ActiveMeetings
from gms.net import SocketIoEndpoint


class MeetingServerApplication:
    """GEM Meeting Server application."""

    def __init__(self):
        """Initialize new instance of the MeetingServerApplication class."""
        super().__init__()

        self.__endpoint = SocketIoEndpoint("0.0.0.0", 8090)
        self.__endpoint.event.subscribe(self.__on_endpoint_event)
        self.__active_meetings = ActiveMeetings(self.__endpoint)

        self.__log = getLogger("communication")

    def __on_endpoint_event(self, event, *data):
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
            self.__log.error("Unable to execute command: %s", str(exc))
            self.__log.exception(exc)
            return {"success": False, "message": "Unknown error: {}".format(str(exc))}

    def run(self):
        """Run application."""
        self.__endpoint.open()
