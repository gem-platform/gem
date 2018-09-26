from inspect import getmembers, isfunction

from gem.core import Processor, Event
from gms.app.context import Context
from gms.net.serializers.meeting import MeetingStageSerializer
from gms.app._fill_meeting import fill_meeting
from gms.meeting.stages import MeetingStages

import gms.commands as commands


class ActiveMeeting:
    """Active meeting."""

    def __init__(self, meeting_id=None):
        """
        Initialize new instance of the ActiveMeeting class.

        Arguments:
            meeting_id {str} -- Meeting id.
        """
        # create execution context
        self.__meeting_id = meeting_id
        self.__context = Context(meeting=self)
        self.__context.send_message.subscribe(self.__on_send_message)
        self.__context.sessions.changed.subscribe(self.__on_sessions_changed)

        # configure meeting stages
        self.__stages = MeetingStages()
        self.__stages.switched.subscribe(self.__on_stage_changed)
        self.__stages.changed.subscribe(self.__on_stage_changed)

        self.__proposals = []
        self.__allowed_users = []
        self.start = None
        self.end = None

        # configure processor:
        # get list of all functions in module
        processor_handlers = getmembers(commands, isfunction)

        # and register them as handler: func_name -> func
        self.__processor = Processor(self.__context)
        self.__processor.register_handlers(processor_handlers)

        # events
        self.__state_changed = Event()
        self.__send_message = Event()

        if meeting_id is not None:
            fill_meeting(self, meeting_id)

    @property
    def context(self):
        """
        Returns meeting context.

        Returns:
            Object -- User defined context.
        """
        return self.__context

    @property
    def stages(self):
        return self.__stages

    @property
    def proposals(self):
        # todo: return readonly
        return self.__proposals

    @property
    def allowed_users(self):
        # todo: return readonly
        return self.__allowed_users


    # Events

    @property
    def state_changed(self):
        """
        Retrun state changed event.

        Returns:
            Event -- State changed.
        """
        return self.__state_changed

    @property
    def send_message(self):
        """
        Retrun send event.

        Returns:
            Event -- Send message event.
        """
        return self.__send_message

    @property
    def meeting_id(self):
        """
        Return meeting ID.

        Returns:
            str -- Meeting ID
        """
        return self.__meeting_id

    def command(self, event, *data):
        """
        Command to execute

        Arguments:
            event {str} -- Command.

        Returns:
            obj -- Result of execution.
        """
        return self.__processor.exec(event, *data)

    def __on_stage_changed(self, index, stage):
        """
        State of the a stage has been changed.

        Arguments:
            index {int} -- Index of the changed stage.
            stage {MeetingStage} -- Meeting stage.
        """
        # stage changed, serialize it
        serializer = MeetingStageSerializer()
        stage_state = serializer.serialize(stage)

        # send serialized data to all connected
        # clients using all endpoints
        self.state_changed.notify({"index": index, "state": stage_state})

    def __on_sessions_changed(self):
        """
        List of active sessions are changed.
        Update list of online users for clients.
        """
        state = self.__context.sessions.state
        self.send_message.notify("meeting_users_online", state)

    def __on_send_message(self, message, data, to=None):
        """Send message requested."""
        self.send_message.notify(message, data, to)