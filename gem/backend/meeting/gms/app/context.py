"""Meeting execution context class."""

from gms.app.sessions import Sessions
from gem.core import Event
from gem.db import User


class Context:
    """Execution context."""

    def __init__(self, meeting):
        """
        Initialize new instance of the Context class.

        Keyword Arguments:
            meeting {ActiveMeeting} -- Meeting.
        """
        self.__meeting = meeting
        self.__sessions = Sessions()
        self.send_message = Event()
        self.__inactive_users = []
        self.__request_access = []
        self.__request_access_u = {}

    @property
    def meeting(self):
        """
        Return meeting.

        Returns:
            Meeting -- Meeting.
        """
        return self.__meeting

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

    @property
    def inactive_users(self):
        return self.__inactive_users

    def find_user(self, id):
        return User.objects.get(pk=id)

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
        users = filter(lambda x: str(x.id) == token, allowed_users)
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
        users = filter(lambda x: str(x.id) == user_id,
                       self.__meeting.allowed_users)
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

    def set_user_inactivity_status(self, user, inactive):
        user_id = str(user.id)
        user_was_inactive = user_id in self.__inactive_users

        # inactive user
        if inactive and not user_was_inactive:
            self.__inactive_users.append(user_id)

        # user is active now
        if not inactive and user_was_inactive:
            self.__inactive_users.remove(user_id)

    # actions

    def close_meeting(self):
        # move all proposals to the next stage
        for proposal in self.meeting.proposals:
            # skip if no workflow or workflow stages specified
            if not (proposal.workflow and proposal.workflow.stages):
                continue

            # get workflow data
            stages = proposal.workflow.stages
            stage = proposal.stage

            try:
                # calculate index
                current_index = stages.index(stage)
                next_index = current_index + 1

                # set next stage from workflow
                if next_index <= len(stages) - 1:
                    proposal.stage = stages[next_index]
                    proposal.save()
            except ValueError:
                pass

    def send(self, message, data, to=None):
        self.send_message.notify(message, data, to)
    
    #
    def request_access(self, sid, user):
        if user not in self.__request_access:
            self.__request_access.append(user)
        
        self.__request_access_u[user.id] = sid

        online = map(lambda u: { "name": str(u.name), "id": str(u.id) }, self.__request_access)
        self.send_message.notify("meeting_users_queue", list(online))
    
    def request_access_sid(self, user):
        return self.__request_access_u.get(user.id, None)
