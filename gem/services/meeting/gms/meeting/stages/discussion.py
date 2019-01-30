"""Discussion stage of the meeting."""

from gms.meeting.stages import MeetingStage


class DiscussionMeetingStage(MeetingStage):
    """Discussion stage of the meeting."""

    def __init__(self, group=None):
        """
        Initialize new instance of the DiscussionMeetingStage class.

        Keyword Arguments:
            group {StagesGroup} -- Group of the stage. (default: {None})
        """
        super().__init__(group=group)
        self.__queue = []
        self.__speaker = None

    @property
    def queue(self):
        """
        Return users in queue.

        Returns:
            list[User] -- List of users.
        """
        return self.__queue

    @property
    def speaker(self):
        """
        Return user is speaking.

        Returns:
            User -- User is speaking now, or None.
        """
        return self.__speaker

    def request_floor(self, user):
        """
        Request a floor.

        Arguments:
            user {User} -- Request a floor.
        """
        # user already in the queue
        if user in self.__queue:
            return

        self.__queue.append(user)
        self.changed.notify()

    def withdraw_from_queue(self, user):
        """
        Remove user from queue.

        Arguments:
            user {User} -- User to remove from queue.
        """
        # user is not in the queue
        if user not in self.__queue:
            return

        # Set speaker to None if he is removed from queue
        if self.__speaker == user:
            self.__speaker = None

        self.__queue.remove(user)
        self.changed.notify()

    def give_voice(self, user):
        """
        Give user a voice.

        Arguments:
            user {User} -- User to get a voice.
        """
        self.__speaker = user
        self.changed.notify()
