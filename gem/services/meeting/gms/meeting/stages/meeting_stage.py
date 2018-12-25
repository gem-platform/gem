"""Abstract meeting stage to inherit all meeting stages from."""

from abc import ABCMeta
from gem.core import Event


class MeetingStage(metaclass=ABCMeta):
    """Meeting stage."""

    def __init__(self, group=None):
        """
        Initialize new instance of the MeetingStage class.

        Arguments:
            meeting {Meeting} -- Meeting.

        Keyword Arguments:
            group {StageGroup} -- Group of the stage. (default: {None})
        """
        self.__group = group
        self.__changed = Event()
        self.__config = {}

    @property
    def group(self):
        """
        Return group of the stage.

        Returns:
            StageGroup -- Group.
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
    def changed(self):
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
