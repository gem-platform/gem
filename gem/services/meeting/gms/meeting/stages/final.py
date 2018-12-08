"""Final stage of the meeting."""

from gms.meeting.stages import MeetingStage


class FinalMeetingStage(MeetingStage):
    """Final stage of the meeting."""

    def __init__(self, group=None):
        """
        Initialize new instance of the FinalMeetingStage class.

        Keyword Arguments:
            group {StageGroup} -- Group of the stage. (default: {None})
        """
        super().__init__(group=group)
