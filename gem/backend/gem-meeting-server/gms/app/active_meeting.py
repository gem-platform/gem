from inspect import getmembers, isfunction

from gem.core import Processor, Event
from gms.app.context import Context
from gms.meeting import Meeting
from gms.net.serializers.meeting import MeetingStageSerializer
from gms.app._fill_meeting import fill_meeting

import gms.commands as commands


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
        self.__context.broadcast.subscribe(self.__on_broadcast)
        self.__context.sessions.changed.subscribe(self.__on_sessions_changed)

        # configure meeting
        self.__meeting = Meeting(self.__context)
        self.__meeting.stages.switch.subscribe(self.__on_stage_changed)
        self.__meeting.stages.changed.subscribe(self.__on_stage_changed)

        # configure processor:
        # get list of all functions in module
        processor_handlers = getmembers(commands, isfunction)

        # and register them as handler: func_name -> func
        self.__processor = Processor(self.__context)
        self.__processor.register_handlers(processor_handlers)

        # events
        self.__state_changed = Event()
        self.__broadcast = Event()

        fill_meeting(self.__meeting, meeting_id)

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
    def broadcast(self):
        """
        Retrun broadcast event.

        Returns:
            Event -- Send broadcast message event.
        """
        return self.__broadcast

    @property
    def meeting_id(self):
        """
        Return meeting ID.

        Returns:
            str -- Meeting ID
        """
        return self.__meeting_id

    @property
    def context(self):
        """
        Retrun execution context.

        Returns:
            Context -- Execution context.
        """
        return self.__context

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
        online = map(lambda u: str(u.id), self.__context.sessions.online)
        self.broadcast.notify("meeting_users_online", list(online))

    def __on_broadcast(self, message, data):
        """Send broadcast message requested."""
        self.broadcast.notify(message, data)
