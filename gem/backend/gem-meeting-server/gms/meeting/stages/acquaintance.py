"""Stage of acquaintance with the document."""

from gms.meeting.stages import MeetingStage


class AcquaintanceMeetingStage(MeetingStage):
    """Acquaintance stage of the meeting."""

    def __init__(self, ballot, comments, group=None):
        """
        Initialize new instance of the AcquaintanceMeetingStage class.

        Keyword Arguments:
            group {StageGroup} -- Group of the stage. (default: {None})
        """
        super().__init__(group=group)
        self.__progress = {}
        self.__ballot = ballot
        self.__comments = comments

    @property
    def progress(self):
        return self.__progress

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
            [Comment] -- List of comments.
        """
        return self.__comments

    def set_progress(self, user, quantity):
        self.__progress[str(user.id)] = quantity
        self.changed.notify()

    def set_online(self, users):
        not_added_users = filter(lambda x: str(x.id) not in self.__progress, users)
        for user in not_added_users:
            self.__progress[str(user.id)] = 0
