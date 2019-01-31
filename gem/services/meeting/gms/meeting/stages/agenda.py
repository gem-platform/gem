"""Agenda stage of the meeting."""

from gms.meeting.stages import MeetingStage


class AgendaMeetingStage(MeetingStage):
    """Agenda stage of the meeting."""

    def __init__(self, content=None, group=None):
        """
        Initialize new instance of the AgendaMeetingStage class.

        Keyword Arguments:
            content {str} -- Content of agenda. (default: {None})
            group {StagesGroup} -- Group of the stage. (default: {None})
        """
        super().__init__(group=group)
        self.__content = content

    @property
    def content(self):
        """
        Return content of agenda.

        Returns:
            str -- Content.
        """
        return self.__content
