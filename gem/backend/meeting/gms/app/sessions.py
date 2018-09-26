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
        self.__meta.changed.subscribe(lambda: self.__changed.notify())

        self.__requests = SessionsAccessRequests()
        self.__requests.changed.subscribe(lambda: self.__changed.notify())

    @property
    def requests(self):
        return self.__requests

    @property
    def meta(self):
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
        online = map(lambda x: { "id": str(x.id), "name": x.name, "role": x.main_role.name, "meta": self.__meta.get(x) }, self.online)
        requests = map(lambda x: { "id": str(x.id), "name": x.name, "role": x.main_role.name }, self.__requests.all)
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
    def __init__(self):
        self.__request_access = []
        self.__request_access_u = {}
        self.__changed = Event()

    @property
    def changed(self):
        return self.__changed

    @property
    def all(self):
        return self.__request_access 

    def add(self, sid, user):
        if user not in self.__request_access:
            self.__request_access.append(user)
        
        self.__request_access_u[user] = sid
        self.__changed.notify()

    def remove(self, user):
        if user in self.__request_access:
            self.__request_access.remove(user)

    def sid(self, user):
        return self.__request_access_u.get(user, None)


class SessionsMeta:
    def __init__(self):
        self.__meta = {}
        self.__changed = Event()

    @property
    def changed(self):
        return self.__changed

    def set(self, user, key, value):
        meta = self.__meta.get(user, None)
        if not meta:
            self.__meta[user] = {}

        self.__meta[user][key] = value
        self.__changed.notify()

    def get(self, user):
        return self.__meta.get(user, None)