"""Stage to display results of the ballot."""

from gms.meeting.stages import MeetingStage


class BallotResultsMeetingStage(MeetingStage):
    """Ballot results stage of the meeting."""

    def __init__(self, ballot, group=None):
        """
        Initialize new instance of the BallotResultsMeetingStage class.

        Arguments:
            ballot {Ballot} -- Ballot.

        Keyword Arguments:
            group {StageGroup} -- Group of the stage. (default: {None})
        """
        super().__init__(group=group)
        self.__ballot = ballot

    @property
    def ballot(self):
        """
        Return ballot.

        Returns:
            Ballot -- Ballot.
        """
        return self.__ballot
