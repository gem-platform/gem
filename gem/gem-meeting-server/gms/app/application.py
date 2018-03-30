from gem.core import Application
from gms.app.context import Context
from gms.commands.handshake import connect, disconnect, handshake
from gms.commands.stages import *
from gms.meeting import Meeting
from gms.net.serializers.meeting import MeetingStageSerializer
from gms.app._fill_meeting import fill_meeting


class MeetingServerApplication(Application):
    """GEM Meeting Server application."""

    def __init__(self):
        """Initialize new instance of the MeetingServerApplication class."""
        super().__init__()

        # create execution context
        self.__context = Context()

        # configure meeting
        self.__meeting = Meeting(self.__context)
        self.__meeting.stages.switch.subscribe(self.__on_stage_changed)
        self.__meeting.stages.changed.subscribe(self.__on_stage_changed)
        self.__context.meeting = self.__meeting

        # todo: MP-11 Fill meeting with real data
        fill_meeting(self.__meeting)

        # configure commands processor
        self.processor.context = self.__context
        self.processor.register_handlers([
            connect, disconnect, handshake, switch_stage, vote, comment,
            request_floor, withdraw_from_queue, remove_from_queue, give_voice])

    def __on_stage_changed(self, index, stage):
        """Call when stage is changed."""
        # stage changed, so serialize it
        serializer = MeetingStageSerializer()
        stage_state = serializer.serialize(stage)

        # send serialized data to all connected
        # clients using all endpoints
        for endpoint in self.endpoints.all:
            endpoint.emit("stage", {"index": index, "state": stage_state})
