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

    @property
    def progress(self):
        """
        Return progress of the ballot stage.

        Returns:
            float -- Progress in percents.
        """
        # it's impossible to calculate percentage without context
        # (we need: users online) so raise an exception
        if not self.meeting.context:
            raise Exception("No context provided")

        # gets list of online users using meeting context
        context = self.meeting.context
        users_online = context.sessions.online
        users_can_vote = self.__users_can_vote(users_online)

        # no one user can vote here
        if len(users_can_vote) <= 0:
            return 0

        # calculate the percentage of completion
        votes_count = len(self.__ballot.votes)
        users_count = len(users_can_vote)
        percent = votes_count / users_count * 100

        # return calculated percent
        return percent

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

    @staticmethod
    def __users_can_vote(users):
        return list(filter(lambda user: "vote" in user.permissions, users))
