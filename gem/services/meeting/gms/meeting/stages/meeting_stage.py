"""Abstract meeting stage to inherit all meeting stages from."""

from abc import ABCMeta
from gem.db import MeetingStageState
from gem.core import Event
from gms.meeting.stages.group import StagesGroup


class MeetingStage(metaclass=ABCMeta):
    """Meeting stage."""

    def __init__(self, state: MeetingStageState = None, group: StagesGroup = None):
        """
        Initialize new instance of the MeetingStage class.

        Keyword Arguments:
            state {MeetingStageState} –– Persistent state.
            group {StagesGroup} -- Group of the stage. (default: {None})
        """
        self.__group = group
        self.__config = {}
        self.__state = state

        # Events
        self.__changed = Event()

    @property
    def state(self) -> MeetingStageState:
        """
        Returns persistent state.

        Returns:
            MeetingStageState -- Persistent state.
        """
        return self.__state

    @property
    def group(self) -> StagesGroup:
        """
        Return group of the stage.

        Returns:
            StagesGroup -- Group.
        """
        return self.__group

    @property
    def meeting(self):
        """
        Return meeting to which it belongs.

        Returns:
            Meeting -- Meeting.
        """
        return self.__group.meeting

    @property
    def changed(self) -> Event:
        """
        Raise when stage changed.

        Returns:
            Event -- Stage changed event.
        """
        return self.__changed

    @property
    def config(self):
        """
        User defined configuration.

        Returns:
            Dict -- User defined configuration.
        """
        return self.__config

    @config.setter
    def config(self, value):
        """
        Sets user defined configuration.
        """
        self.__config = value


    def on_enter(self):
        """
        Called when stage activated.
        """

    def on_leave(self):
        """
        Called when stage deactivated.
        """
