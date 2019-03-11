from logging import getLogger
from gem.core import Event
from gms.app.active_meeting import ActiveMeeting
from gms.app.active_meeting_connections import ActiveMeetingConnections


CLOG = getLogger("communication")

class Intercom:
    def __init__(self, meeting_id, endpoint):
        self.__meeting_id = meeting_id
        self.__endpoint = endpoint

    def emit(self, event, *data, to=None):
        CLOG.debug("-X-> %s %s %s", event, data, to or self.__meeting_id)
        self.__endpoint.emit(event, data, to or self.__meeting_id)


    def join(self, sid, room):
        self.__endpoint.join(sid, room)

    def leave(self, sid, room):
        self.__endpoint.leave(sid, room)


class ActiveMeetings:
    """
    Active meetings manager.
    """

    def __init__(self, endpoint):
        """Initialize new instance of the ActiveMeetings class."""
        self.__endpoint = endpoint

        self.__active = {}  # active meetings keyed by meeting_id
        self.__connections = ActiveMeetingConnections()
        self.__status_changed = Event()

        self.__comm_log = getLogger("communication")
        self.__meetings_log = getLogger("meetings")

    @property
    def status_changed(self):
        """
        Status of active meetings changed.

        Returns:
            Event -- Event.
        """
        return self.__status_changed

    def __status(self):
        status = list(self.__active.keys())
        online = {k: len(v.sessions.online) for k, v in self.__active.items()}
        return {"active": status, "online": online}

    def command(self, event, *data):
        sid = data[0]
        result = None

        self.__comm_log.debug("%s => %s %s", sid, event, data)

        if event == "meetings_status":
            return self.__status()

        # handshake command received, so open meeting (if not)
        # and join user to specified room
        if event == "handshake":
            self.__on_handshake(sid, data)

        # get meeting of specified user and pass command to it
        meeting = self.__connections.get_meeting(sid)
        if meeting:
            result = meeting.command(event, *data)

        # Meeting for specified SID closed already
        if not meeting and event not in ["disconnect", "handshake"]:
            return {"success": False, "message": "Your sessions is outdated"}

        # process meeting "disconnect" command first
        if event == "disconnect":
            self.__on_disconnect(sid)

        if event in ["handshake", "disconnect"]:
            self.status_changed.notify(self.__status())

        return result

    def __open_meeting(self, meeting_id):
        # lookup for open meetings
        exist = self.__active.get(meeting_id, None)
        if exist:
            return exist

        # no active meetings with specified ID found, so open new one
        self.__meetings_log.debug("Opening new meeting %s", meeting_id)
        new_intercom = Intercom(meeting_id, self.__endpoint)
        new_meeting = ActiveMeeting(meeting_id, new_intercom)
        # todo: unsubscribe then meeting closed in __close_empty_meetings
        new_meeting.closed.subscribe(self.__on_meeting_closed)
        self.__active[meeting_id] = new_meeting
        return new_meeting


    def __on_handshake(self, sid, data):
        command_data = data[1]  # todo: data may not be specified
        meeting_id = command_data.get("meeting", None)
        if not meeting_id:
            raise Exception("No meeting ID provided")

        # user already connected to some meeting
        # disconnect him from previous one first
        if self.__connections.is_connected(sid):
            self.__meetings_log.debug("Remove %s from previous meeting.", sid)
            prev_meeting = self.__connections.get_meeting(sid)
            prev_meeting.sessions.delete(sid)
            self.__endpoint.leave(sid, prev_meeting.meeting_id)

        # get meeting by specified id
        # open new one of not exist
        meeting = self.__open_meeting(meeting_id)
        self.__connections.connect(sid, meeting)
        self.__endpoint.join(sid, meeting_id)

    def __on_disconnect(self, sid):
        self.__connections.disconnect(sid)

    def __on_meeting_closed(self, meeting):
        del self.__active[meeting.meeting_id]
        self.__connections.close_meeting(meeting)
