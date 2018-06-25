"""Stage of acquaintance with the document."""

from gms.meeting.stages import MeetingStage


class AcquaintanceMeetingStage(MeetingStage):
    """Acquaintance stage of the meeting."""

    def __init__(self, ballot, comments, group=None):
        """
        Initialize new instance of the AcquaintanceMeetingStage class.

        Arguments:
            ballot {Ballot} -- Ballot from previous stage of proposal
            comments {Comments} -- Comments from previous stage of proposal

        Keyword Arguments:
            group {StageGroup} -- Group of the stage. (default: {None})
        """
        super().__init__(group=group)
        self.__progress = {}
        self.__ballot = ballot
        self.__comments = comments

    @property
    def progress(self):
        """
        Return progress of reading proposal.

        Returns:
            dict -- Progress { count: NUM, values: { USER_ID: 0-1 } }
        """
        readers_count = len(self.meeting.context.sessions.online)
        return {
            "count": readers_count,
            "values": self.__progress
        }

    @property
    def ballot(self):
        """
        Return ballot.

        Returns:
            Ballot -- Ballot.
        """
        return self.__ballot

    @property
    def comments(self):
        """
        Return comments.

        Returns:
            Comment -- List of comments.
        """
        return self.__comments

    def set_progress(self, user, quantity):
        """
        Set reading progress for specified user

        Arguments:
            user {User} -- User to set progress of
            quantity {float} -- Progress (0-1)
        """
        user_id = str(user.id)
        self.__progress[user_id] = quantity
        self.changed.notify()
