from tribool import Tribool
from gem.core import Event


class Quorum:
    def __init__(self, meeting):
        self.__value = 19
        self.__new_value = -1
        self.__votes = {}
        self.__meeting = meeting
        self.__changed = Event()

    @property
    def changed(self):
        return self.__changed

    @property
    def users_can_change(self):
        return list(filter(lambda x:
                           x.have_permission("meeting.quorum_change",
                                             accept_superuser=False),
                           self.__meeting.allowed_users))

    @property
    def value(self):
        return self.__value

    @property
    def change_approved_by(self):
        return list(self.__votes.keys())

    def request_change(self, value):
        self.__votes = {}
        self.__new_value = value

    def vote_change(self, user, value) -> Tribool:
        self.__votes[str(user.id)] = value

        if value is False:  # ballot should be unanimous
            return Tribool(False)

        # change is approved
        # all of users are voted
        users_voted = len(self.__votes.keys())
        votes_required = len(self.users_can_change)
        if users_voted == votes_required:
            self.__value = self.__new_value
            self.changed.notify()
            return Tribool(True)

        # indeterminate
        return Tribool(None)
        