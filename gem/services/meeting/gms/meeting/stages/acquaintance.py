"""Stage of acquaintance with the document."""

from gms.meeting.stages import MeetingStage


class AcquaintanceMeetingStage(MeetingStage):
    """Acquaintance stage of the meeting."""

    def __init__(self, ballot, comments, state=None, group=None):
        """
        Initialize new instance of the AcquaintanceMeetingStage class.

        Arguments:
            ballot {Ballot} -- Ballot to display results of.
            comments {list[Comments]} -- List of comments to display.

        Keyword Arguments:
            state {MeetingStageState} –– Persistent state.
            group {StagesGroup} -- Group of the stage. (default: {None})
        """
        super().__init__(state=state, group=group)
        self.__ballot = ballot
        self.__comments = comments

        # seed state if empty
        if not hasattr(self.state, "progress"):
            self.state.progress = {}

    @property
    def progress(self):
        """
        Return progress of reading proposal.

        Returns:
            dict -- Progress { count: NUM, values: { USER_ID: 0-1 } }
        """
        readers_count = len(self.meeting.allowed_users)
        return {
            "count": readers_count,
            "values": self.state.progress
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
        Set reading progress for specified user.

        Arguments:
            user {User} -- User to set progress of
            quantity {float} -- Progress (0-1)
        """
        self.state.progress[str(user.id)] = quantity
        self.state.save()
        self.changed.notify()

    def get_progress(self, user):
        """
        Get reading progress for specified user.

        Arguments:
            user {User} -- User to get reading progress of.

        Returns:
            float -- Progress (0-1)
        """
        return self.state.progress.get(str(user.id), 0)
