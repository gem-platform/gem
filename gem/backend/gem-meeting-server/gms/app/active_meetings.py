from gem.core import Event
from gms.app.active_meeting import ActiveMeeting


class ActiveMeetings:
    """
    Active meetings manager.
    """

    def __init__(self):
        """Initialize new instance of the ActiveMeetings class."""
        self.__emit = Event()
        self.__join = Event()
        self.__leave = Event()
        self.__active = {}  # active meetings keyed by meeting_id
        self.__connection = {}  # session_id -> active meeting
        self.__status_changed = Event()

    @property
    def status_changed(self):
        return self.__status_changed

    @property
    def emit(self):
        """Return emit event."""
        return self.__emit

    @property
    def join(self):
        """Return join event."""
        return self.__join

    @property
    def leave(self):
        """Return leave event."""
        return self.__leave

    def status(self):
        status = list(self.__active.keys())
        online = {k: len(v.context.sessions.online) for k, v in self.__active.items()}
        return {"active": status, "online": online}

    def command(self, event, *data):
        sid = data[0]
        result = None

        if event == "meetings_status":
            return self.status()

        # handshake command received, so open meeting (if not)
        # and join user to specified room
        if event == "handshake":
            self.__on_handshake(sid, data)

        # get meeting of specified user and
        # pass command to it
        meeting = self.__connection.get(sid, None)
        if meeting:
            result = meeting.command(event, *data)

        # process meeting "disconnect" command first
        if event == "disconnect":
            self.__on_disconnect(sid)

        if event in ["handshake", "disconnect"]:
            self.status_changed.notify()

        return result

    def __open_meeting(self, meeting_id):
        # lookup for open meetings
        exist = self.__active.get(meeting_id, None)
        if exist:
            return exist

        # no active meetings with specified id found
        # open new one
        new_meeting = ActiveMeeting(meeting_id)
        new_meeting.state_changed.subscribe(self.__state_changed(meeting_id))
        new_meeting.broadcast.subscribe(self.__broadcast(meeting_id))
        self.__active[meeting_id] = new_meeting
        return new_meeting

    def __state_changed(self, meeting_id):
        def handler(data):
            self.emit.notify("stage", data, meeting_id)
        return handler

    def __broadcast(self, meeting_id):
        def handler(message, data):
            self.emit.notify(message, data, meeting_id)
        return handler

    def __on_handshake(self, sid, data):
        command_data = data[1]  # todo: data may not be specified
        meeting_id = command_data.get("meeting")

        # user already connected to some meeting
        # disconnect him from previous one first
        if sid in self.__connection:
            prev_meeting = self.__connection[sid]
            prev_meeting.context.sessions.delete(sid)
            self.__leave.notify(sid, prev_meeting.meeting_id)

        # get meeting by specified id
        # open new one of not exist
        meeting = self.__open_meeting(meeting_id)
        self.__connection[sid] = meeting
        self.__join.notify(sid, meeting_id)

    def __on_disconnect(self, sid):
        # remove user connection
        if sid in self.__connection:
            del self.__connection[sid]

        # stop active meetings if no connections
        meetings_to_close = [m.meeting_id for m in self.__active.values()
                             if not m.context.sessions.online]

        # stop inactive meetings
        for meeting_id in meetings_to_close:
            del self.__active[meeting_id]
