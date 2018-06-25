from gem.core import Event


class Sessions:
    """Stores associations between session ID and user."""

    def __init__(self):
        """Initializes new instance of the Sessions class."""
        self.__sessions = {}
        self.__changed = Event()

    @property
    def changed(self):
        return self.__changed

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
        self.__sessions[session_id] = user
        self.__changed.notify()

    def delete(self, session_id):
        """
        Logins user out by specified token.

        Arguments:
            session_id {str} -- Session id.
        """
        if session_id in self.__sessions:
            del self.__sessions[session_id]
            self.__changed.notify()
