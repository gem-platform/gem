from gem.core import Event

from gms.meeting.stages import MeetingStages 


class Meeting:
    """Meeting model."""

    def __init__(self, context=None):
        """Initialize new instance of the Meeting class."""
        self.__stages = MeetingStages()
        self.__proposals = []
        self.__allowed_users = []
        self.__context = context
        self.__context.meeting = self
        self.start = None
        self.end = None

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

