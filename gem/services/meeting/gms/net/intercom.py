"""Intercom class. Provides communication between server and client through specified endpoint."""
from logging import getLogger
from gem.core import Endpoint


class Intercom:
    """Provides communication between server and client."""

    def __init__(self, meeting_id: str, endpoint: Endpoint):
        """
        Initialize a new instance of an Intercom class.

        Arguments:
            meeting_id {str} -- Meeting Id.
            endpoint {Endpoint} -- The endpoint to communicate through.
        """
        self.__log = getLogger("communication")
        self.__meeting_id = meeting_id
        self.__endpoint = endpoint

    def emit(self, event: str, data: object, to: str = None):
        """
        Send data to client.

        Arguments:
            event {str} -- Type of event.
            data {dict} -- Data to send.

        Keyword Arguments:
            to {str} -- Receiver. (default: {None})
                        None -- will send to meeting room only.
                        '@all' --  to send to all connected clients.
        """
        self.__log.debug("--> %s %s to: %s", event, data, to or self.__meeting_id)
        room_to_send = None if to == "@all" else to or self.__meeting_id
        self.__endpoint.emit(event, data, room_to_send)

    def join(self, sid, room):
        """Join session to room.

        Arguments:
            sid {str} -- Session Id.
            room {str} -- Room Id.
        """
        self.__endpoint.join(sid, room)

    def leave(self, sid, room):
        """Remove session from room.

        Arguments:
            sid {str} -- Session Id.
            room {str} -- Room Id.
        """
        self.__endpoint.leave(sid, room)
