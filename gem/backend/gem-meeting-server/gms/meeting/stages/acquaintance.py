"""Stage of acquaintance with the document."""

from gms.meeting.stages import MeetingStage


class AcquaintanceMeetingStage(MeetingStage):
    """Acquaintance stage of the meeting."""

    def __init__(self, group=None):
        """
        Initialize new instance of the AcquaintanceMeetingStage class.

        Keyword Arguments:
            group {StageGroup} -- Group of the stage. (default: {None})
        """
        super().__init__(group=group)
