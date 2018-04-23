from inspect import getmembers, isfunction

from gem.core import Processor, Event
from gms.app.context import Context
from gms.meeting import Meeting
from gms.net.serializers.meeting import MeetingStageSerializer
from gms.app._fill_meeting import fill_meeting

import gms.commands as commands


class ActiveMeetings:
    """Active meetings."""

    def __init__(self):
        """Initialize new instance of the ActiveMeetings class."""
        self.__emit = Event()
        self.__join = Event()
        self.__leave = Event()
        self.__active = {}  # active meetings keyed by meeting_id
        self.__connection = {}  # user_id -> active meeting

    @property
    def emit(self):
        return self.__emit

    @property
    def join(self):
        return self.__join

    @property
    def leave(self):
        return self.__leave

    def command(self, event, *data):
        sid = data[0]

        # handshake command received, so open meeting (if not)
        # and join user to specified room
        if event == "handshake":
            command_data = data[1]  # todo: data may not be specified
            meeting_id = command_data.get("meeting")

            # user already connected to some meeting
            if sid in self.__connection:
                prev_meeting = self.__connection[sid]
                self.__leave.notify(sid, prev_meeting.meeting_id)

            self.__connection[sid] = self.__open_meeting(meeting_id)
            self.__join.notify(sid, meeting_id)
        if event == "disconnect":
            from collections import Counter
            c = Counter(self.__connection)
            print(dict(c.items()))

            # remove user connection
            if sid in self.__connection:
                del self.__connection[sid]

            # stop active meetings if no connections
            meetings_to_close = []
            for meeting_id, active_meeting in self.__active.items():
                count = 0
                for sid, connected_meeting in self.__connection.items():
                    if active_meeting == connected_meeting:
                        count += 1
                if count == 0:
                    meetings_to_close.append(meeting_id)

            for meeting_id in meetings_to_close:
                del self.__active[meeting_id]

        # get meeting of specified user and
        # pass command to it
        meeting = self.__connection.get(sid, None)
        if meeting:
            return meeting.command(event, *data)

    def __open_meeting(self, meeting_id):
        # lookup for open meetings
        exist = self.__active.get(meeting_id, None)
        if exist:
            return exist

        # no active meetings with specified id found
        # open new one
        new_meeting = ActiveMeeting(meeting_id)
        new_meeting.state_changed.subscribe(self.__state_changed(meeting_id))
        self.__active[meeting_id] = new_meeting
        return new_meeting

    def __state_changed(self, meeting_id):
        def handler(data):
            self.emit.notify(meeting_id, data)
        return handler


class ActiveMeeting:
    """Active meeting."""

    def __init__(self, meeting_id):
        """
        Initialize new instance of the ActiveMeeting class.

        Arguments:
            meeting_id {str} -- Meeting id.
        """

        # create execution context
        self.__meeting_id = meeting_id
        self.__context = Context()

        # configure meeting
        self.__meeting = Meeting(self.__context)
        self.__meeting.stages.switch.subscribe(self.__on_stage_changed)
        self.__meeting.stages.changed.subscribe(self.__on_stage_changed)

        # configure processor:
        # get list of all functions in module
        # and register them as handler: func_name.__name__ -> func_name
        self.__processor = Processor()
        self.__processor.context = self.__context
        self.__processor.register_handlers(
            [o[1] for o in getmembers(commands, isfunction)])

        # events
        self.__state_changed = Event()

        # todo: MP-11 Fill meeting with real data
        fill_meeting(self.__meeting)

    @property
    def meeting_id(self):
        return self.__meeting_id

    @property
    def state_changed(self):
        """State changed event."""
        return self.__state_changed

    def command(self, event, *data):
        """Command to execute."""
        return self.__processor.exec(event, *data)

    def __on_stage_changed(self, index, stage):
        """Call when stage is changed."""
        # stage changed, so serialize it
        serializer = MeetingStageSerializer()
        stage_state = serializer.serialize(stage)

        # send serialized data to all connected
        # clients using all endpoints
        self.state_changed.notify({"index": index, "state": stage_state})
