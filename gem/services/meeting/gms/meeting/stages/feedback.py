"""Final stage of the meeting."""

from gms.meeting.stages import (MeetingStage, AcquaintanceMeetingStage, BallotMeetingStage,
                                CommentsMeetingStage)


class FeedbackMeetingStage(MeetingStage):
    """Feedback stage of the meeting."""

    def __init__(self, ballot, comments, group=None):
        """
        Initialize new instance of the FeedbackMeetingStage class.

        Keyword Arguments:
            group {StageGroup} -- Group of the stage. (default: {None})
        """
        super().__init__(group=group)
        self.__acquaintance = AcquaintanceMeetingStage(ballot, comments, group=group)
        self.__comments = CommentsMeetingStage(comments, group=group)
        self.__ballot = BallotMeetingStage(ballot, group=group)

    def comment(self, user, message, mark, quote=None):
        return self.__comments.comment(user, message, mark, quote=quote)

    @property
    def progress(self):
        """
        Return progress of reading proposal.

        Returns:
            dict -- Progress { count: NUM, values: { USER_ID: 0-1 } }
        """
        return self.__acquaintance.progress

    @property
    def ballot(self):
        """
        Return ballot.

        Returns:
            Ballot -- Ballot.
        """
        return self.__ballot.ballot

    @property
    def comments(self):
        """
        Return comments.

        Returns:
            Comment -- List of comments.
        """
        return self.__comments.comments

    def set_progress(self, user, quantity):
        """
        Set reading progress for specified user

        Arguments:
            user {User} -- User to set progress of
            quantity {float} -- Progress (0-1)
        """
        self.__acquaintance.set_progress(user, quantity)
        # self.changed.notify() ???

    @property
    def is_quorum_met(self):
        return True

    def vote(self, user, value):
        """
        Commit specified vote of specified user.

        Arguments:
            user {User} -- User
            value {str} -- Value
        """
        self.__ballot.vote(user, value)

    def on_leave(self):
        """
        Called when stage deactivated.
        """
        self.__ballot.ballot.stage = self.group.proposal.stage
        self.__ballot.ballot.save()
