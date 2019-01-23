"""Ballot."""

from gms.meeting.stages import MeetingStage
from gem.db import OpForbidden


class BallotMeetingStage(MeetingStage):
    """Ballot stage of the meeting."""

    def __init__(self, ballot, group=None, check_quorum=True):
        """
        Initialize new instance of the BallotMeetingStage.

        Arguments:
            ballot {Ballot} -- Ballot model to store results in.

        Keyword Arguments:
            group {StageGroup} -- Group of the stage (default: {None})
        """
        super().__init__(group=group)
        self.__check_quorum = check_quorum
        self.__ballot = ballot
        self.meeting.quorum.changed.subscribe(self.__on_check_quorum)
        self.meeting.sessions.changed.subscribe(self.__on_check_quorum)

    @property
    def check_quorum(self) -> bool:
        """
        Should we check quorum before accepting a vote?

        Returns:
            bool -- True or False.
        """
        return self.__check_quorum

    @check_quorum.setter
    def check_quorum(self, value: bool):
        """
        Set quorum checking value.

        Arguments:
            value {bool} -- True or False.
        """
        self.__check_quorum = value

    @property
    def is_quorum_met(self) -> bool:
        """
        Is quorum met? (Returns True if check_quorum is set to False)

        Returns:
            bool -- True of quorum is met.
        """
        return self.__check_quorum is False or\
            len(self.meeting.sessions.online) >= self.meeting.quorum.value

    @property
    def ballot(self):
        """
        Return ballot model.

        Returns:
            Ballot -- Ballot
        """
        return self.__ballot

    def on_leave(self):
        """
        Called when stage deactivated.
        """
        self.__ballot.stage = self.group.proposal.stage
        self.__ballot.save()

    def vote(self, user, value):
        """
        Commit specified vote of specified user.

        Arguments:
            user {User} -- User
            value {str} -- Value
        """
        if not self.is_quorum_met:
            return (False, "Quorum is not met")

        try:
            self.__ballot.set(user, value)
            self.changed.notify()
            return (True, "Accepted")
        except OpForbidden as exc:
            return (False, str(exc))

    def __on_check_quorum(self):
        """
        Quorum value may be changed.
        """
        self.changed.notify()
