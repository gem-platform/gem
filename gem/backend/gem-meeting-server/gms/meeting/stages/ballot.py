from gms.meeting.stages import MeetingStage


class BallotMeetingStage(MeetingStage):
    """Ballot stage of the meeting."""

    def __init__(self, ballot, group=None):
        """
        Initialize new instance of the BallotMeetingStage.

        Arguments:
            ballot {Ballot} -- Ballot model to store results in.

        Keyword Arguments:
            group {StageGroup} -- Group of the stage (default: {None})
        """
        super().__init__(group=group)
        self.__ballot = ballot

    @property
    def ballot(self):
        """
        Return ballot model.

        Returns:
            Ballot -- Ballot
        """
        return self.__ballot

    def vote(self, user, value):
        """
        Commit specified vote of specified user.

        Arguments:
            user {User} -- User
            value {str} -- Value
        """
        self.__ballot.set(user, value)
        self.changed.notify()
        self.__ballot.save()  # todo: performance fix: save on exit from stage

