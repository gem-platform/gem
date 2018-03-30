from gms.app.sessions import Sessions


class Context:
    """Execution context."""

    def __init__(self):
        """Initialize new instance of the Context class."""
        self.__meeting = None
        self.__sessions = Sessions()

    @property
    def meeting(self):
        """
        Return meeting.

        Returns:
            Meeting -- Meeting.
        """
        return self.__meeting

    @meeting.setter
    def meeting(self, value):
        """
        Set meeting.

        Arguments:
            value {Meeting} -- Meeting.
        """
        self.__meeting = value

    @property
    def stage(self):
        """
        Return current stage of the session.

        Returns:
            MeetingStage -- Current stage of the session.
        """
        return self.meeting.stages.current

    @property
    def sessions(self):
        """
        Return sessions.

        Returns:
            Sessions -- Sessions.
        """
        return self.__sessions

    # User section

    def get_user(self, sid):
        """
        Return user by specified session id.

        Arguments:
            sid {str} -- Session id.

        Returns:
            User -- User associated with specified session.
        """
        return self.__sessions.get(sid)

    def get_user_by_token(self, token):
        """
        Return user by specified credentials.

        Arguments:
            token {str} -- Authentication token.

        Returns:
            User -- User associated with specified token.
        """
        # todo: token != user_id
        allowed_users = self.__meeting.allowed_users
        users = filter(lambda x: x.id == token, allowed_users)
        users = list(users)
        if len(users) == 1:
            return users[0]
        return None

    def get_user_by_id(self, user_id):
        """
        Return user by specified id.

        Arguments:
            user_id {str} -- User id.

        Returns:
            User -- User associated with specified id.
        """
        users = filter(lambda x: x.id == user_id, self.__meeting.allowed_users)
        users = list(users)
        return users[0] if len(users) == 1 else None

    def login_user(self, sid, user):
        """
        Turn user to authenticated state.

        Arguments:
            sid {str} -- Session id.
            user {User} -- User to authenticate.
        """
        self.__sessions.save(sid, user)

    def logout_user(self, sid):
        """
        Turn user to unauthenticated state.

        Arguments:
            sid {str} -- Session id.
        """
        self.__sessions.delete(sid)
