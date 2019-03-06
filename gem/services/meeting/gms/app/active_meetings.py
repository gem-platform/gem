from datetime import datetime
from logging import getLogger
from gem.core import Event
from gms.app.active_meeting import ActiveMeeting
from gms.app.active_meeting_connections import ActiveMeetingConnections


class ActiveMeetings:
    """
    Active meetings manager.
    """

    def __init__(self):
        """Initialize new instance of the ActiveMeetings class."""
        self.__open = Event()
        self.__close = Event()
        self.__emit = Event()
        self.__join = Event()
        self.__leave = Event()
        self.__active = {}  # active meetings keyed by meeting_id
        self.__connections = ActiveMeetingConnections()
        self.__status_changed = Event()

        self.__log = getLogger("root")
        self.__comm_log = getLogger("communication")
        self.__meetings_log = getLogger("meetings")

    @property
    def open(self) -> Event:
        return self.__open

    @property
    def close(self) -> Event:
        return self.__close

    @property
    def status_changed(self):
        """
        Status of active meetings changed.

        Returns:
            Event -- Event.
        """
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
        online = {k: len(v.sessions.online) for k, v in self.__active.items()}
        return {"active": status, "online": online}

    def command(self, event, *data):
        try:
            sid = data[0]
            result = None

            self.__comm_log.debug("%s => %s %s", sid, event, data)

            if event == "meetings_status":
                return self.status()

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
                self.status_changed.notify()

            return result
        except Exception as exc:
            self.__log.error("Unable to execute command: %s", str(exc))
            self.__log.exception(exc)
            return {"success": False, "message": "Unknown error: {}".format(str(exc))}

    def __open_meeting(self, meeting_id):
        # lookup for open meetings
        exist = self.__active.get(meeting_id, None)
        if exist:
            return exist

        # no active meetings with specified ID found, so open new one
        self.__meetings_log.debug("Opening new meeting %s", meeting_id)
        new_meeting = ActiveMeeting(meeting_id)
        # todo: unsubscribe then meeting closed in __close_empty_meetings
        new_meeting.state_changed.subscribe(self.__state_changed(meeting_id))
        new_meeting.stage_switched.subscribe(self.__stage_switched(meeting_id))
        new_meeting.send_message.subscribe(self.__send_message(meeting_id))
        new_meeting.closed.subscribe(self.__on_meeting_closed)
        self.__active[meeting_id] = new_meeting
        self.__open.notify(new_meeting)
        return new_meeting

    def __state_changed(self, meeting_id):
        def handler(data):
            self.__log.critical("SEND STATE" + str(data))
            self.emit.notify("stage", data, meeting_id)
        return handler

    def __stage_switched(self, meeting_id):
        def handler(data):
            self.__log.critical("SEND INDEX" + str(data))
            self.emit.notify("stage_switched", data, meeting_id)
        return handler

    def __send_message(self, meeting_id):
        def handler(message, data, to=None):
            self.__comm_log.debug("< send %s in %s %s %s", to, meeting_id, message, data)
            self.emit.notify(message, data, to or meeting_id)
        return handler

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
            self.__leave.notify(sid, prev_meeting.meeting_id)

        # get meeting by specified id
        # open new one of not exist
        meeting = self.__open_meeting(meeting_id)
        self.__connections.connect(sid, meeting)
        self.__join.notify(sid, meeting_id)

    def __on_disconnect(self, sid):
        self.__connections.disconnect(sid)

    def __on_meeting_closed(self, meeting):
        del self.__active[meeting.meeting_id]
        self.__connections.close_meeting(meeting)
        self.__close.notify(meeting)
