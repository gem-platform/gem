"""Sessions container."""

from logging import getLogger

from gem.core import Event


class Sessions:
    """Stores associations between session ID and user."""

    def __init__(self):
        """Initializes new instance of the Sessions class."""
        self.__sessions = {}
        self.__changed = Event()
        self.__log = getLogger("sessions")

        self.__meta = SessionsMeta()
        self.__requests = SessionsAccessRequests()

        self.__meta.changed.subscribe(self.__changed.notify)
        self.__requests.changed.subscribe(self.__changed.notify)

    @property
    def requests(self):
        """
        Return api to manipulate with access requests.

        Returns:
            SessionsAccessRequests -- Api.
        """
        return self.__requests

    @property
    def meta(self):
        """
        Return api to manipulate with meta.

        Returns:
            SessionsMeta -- Api.
        """
        return self.__meta

    @property
    def changed(self):
        """
        Get changed event

        Returns:
            Event -- Sessions changed
        """
        return self.__changed


    @property
    def state(self):
        """
        Return state of the sessions.

        Returns:
            dict -- State of the session.
        """
        online = map(lambda x: {
            "id": str(x.id), "name": x.name, "role": x.main_role.name, "meta": self.__meta.get(x)
            }, self.online)
        requests = map(lambda x: {
            "id": str(x.id), "name": x.name, "role": x.main_role.name
            }, self.__requests.all)

        return {
            "online": list(online),
            "requests": list(requests)
        }

    @property
    def online(self):
        """
        Returns lists of users online.

        Returns:
            list[User] -- List of users online.
        """
        return list(set(self.__sessions.values()))

    def get(self, sid):
        """
        Returns user by specified session id.

        Arguments:
            sid {str} -- Session id.

        Returns:
            User -- User associated with specified session.
        """
        return self.__sessions.get(sid, None)

    def get_session(self, user):
        filtered = {sid: user for sid, s_user in self.__sessions.items() if user == s_user}
        filtered = list(filtered.keys())
        if len(filtered) == 1:
            return filtered[0]

    def save(self, session_id, user):
        """
        Sets association between session id and user.

        Arguments:
            session_id {str} -- Session id.
            user {User} -- User.
        """
        # remove user from access requests
        self.__requests.remove(user)

        # save
        self.__sessions[session_id] = user
        self.__changed.notify()
        self.__log.debug("Add %s -> %s", user.name, session_id)

    def delete(self, session_id):
        """
        Logins user out by specified token.

        Arguments:
            session_id {str} -- Session id.
        """
        if session_id in self.__sessions:
            self.__log.debug("Delete %s", session_id)
            del self.__sessions[session_id]
            self.__changed.notify()
        else:
            self.__log.error("Unable delete %s", session_id)

    def delete_all(self):
        """Delete all sessions"""
        self.__sessions = {}
        self.__changed.notify()


class SessionsAccessRequests:
    """Access requests."""

    def __init__(self):
        """
        Initializes new instance of the SessionsAccessRequests class.
        """
        self.__queue = []
        self.__sids = {}
        self.__changed = Event()

    @property
    def changed(self):
        """
        Sessions changed event.

        Returns:
            Event -- Sessions has been changed.
        """
        return self.__changed

    @property
    def all(self):
        """
        Returns list of all requests.

        Returns:
            list(User) -- List of users.
        """
        return self.__queue

    def add(self, sid, user):
        """
        Add new user.

        Arguments:
            sid {str} -- Session ID.
            user {User} -- User.
        """
        if user not in self.__queue:
            self.__queue.append(user)

        self.__sids[user] = sid
        self.__changed.notify()

    def remove(self, user):
        """
        Remove user.

        Arguments:
            user {User} -- User.
        """
        if user in self.__queue:
            self.__queue.remove(user)


    def sid(self, user):
        """
        Returns session ID for specified user.

        Arguments:
            user {User} -- [description]

        Returns:
            [type] -- [description]
        """
        return self.__sids.get(user, None)


class SessionsMeta:
    """Keeps meta information for each session."""

    def __init__(self):
        """Initializes new instance of the SessionsMeta class."""
        self.__meta = {}
        self.__changed = Event()

    @property
    def changed(self):
        """
        Meta changed event.

        Returns:
            Event -- Meta has been changed.
        """
        return self.__changed

    def set(self, user, key, value):
        """
        Sets meta for specified user.

        Arguments:
            user {User} -- User to set meta for.
            key {str} -- Key.
            value {obj} -- Value.
        """
        meta = self.__meta.get(user, None)
        if not meta:
            self.__meta[user] = {}

        self.__meta[user][key] = value
        self.__changed.notify()

    def get(self, user):
        """
        Returns value of meta for specified user.

        Arguments:
            user {User} -- Iser to get meta from.

        Returns:
            obj -- Value.
        """
        return self.__meta.get(user, None)
    