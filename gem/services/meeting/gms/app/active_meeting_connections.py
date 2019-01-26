from gms.app.active_meeting import ActiveMeeting


class ActiveMeetingConnections:
    """
    Map between SessionID and ActiveMeeting.
    """

    def __init__(self):
        """Initializes new instance of the ActiveMeetingConnections class."""
        self.__connections = {}

    def connect(self, sid: str, meeting: ActiveMeeting):
        """
        Sets association between SessionID and ActiveMeeting.

        Arguments:
            sid {str} -- SessionID
            meeting {ActiveMeeting} -- Active meeting
        """
        self.__connections[sid] = meeting

    def disconnect(self, sid):
        """
        Removes association between SessionID and ActiveMeeting

        Arguments:
            sid {str} -- SessionID
        """
        if sid in self.__connections:
            del self.__connections[sid]

    def is_connected(self, sid) -> bool:
        """
        Is session connected to any meeting?

        Arguments:
            sid {str} -- SessionID

        Returns:
            bool -- True if connected.
        """
        return sid in self.__connections

    def get_meeting(self, sid) -> ActiveMeeting:
        """Return meeting connected to

        Arguments:
            sid {str} -- SessionID

        Returns:
            ActiveMeeting -- Active meeting session is connected to
        """
        return self.__connections.get(sid, None)

    def close_meeting(self, meeting: ActiveMeeting):
        """
        Remove all associations for specified meeting.

        Arguments:
            meeting {ActiveMeeting} -- Meting to remove all association for.
        """
        self.__connections = {
            k: v for k, v in self.__connections.items()
            if v is not meeting
        }
