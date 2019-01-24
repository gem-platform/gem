from inspect import getmembers, isfunction
from tribool import Tribool

from gem.core import Processor, Event
from gem.db import User

from gms.net.serializers.meeting import MeetingStageSerializer
from gms.net.serializers.meeting import MeetingSerializer
from gms.app._fill_meeting import fill_meeting
from gms.meeting.stages import MeetingStages
from gms.app.sessions import Sessions

import gms.commands as commands


class ActiveMeeting:
    """Active meeting."""

    def __init__(self, meeting_id=None):
        """
        Initialize new instance of the ActiveMeeting class.

        Arguments:
            meeting_id {str} -- Meeting id.
        """
        self.__meeting_id = meeting_id

        # sessions
        self.__sessions = Sessions()
        self.__sessions.changed.subscribe(self.__on_sessions_changed)

        # configure meeting stages
        self.__stages = MeetingStages()
        self.__stages.switched.subscribe(self.__on_stage_changed)
        self.__stages.changed.subscribe(self.__on_stage_changed)

        self.__proposals = []
        self.__allowed_users = []
        self.start = None
        self.end = None
        self.quick_ballot = QuickBallot()
        self.quorum = Quorum(self)

        # configure processor:
        # get list of all functions in module
        processor_handlers = getmembers(commands, isfunction)

        # and register them as handler: func_name -> func
        self.__processor = Processor(self)
        self.__processor.register_handlers(processor_handlers)

        # events
        self.__state_changed = Event()
        self.__send_message = Event()
        self.__closed = Event()

        if meeting_id is not None:
            fill_meeting(self, meeting_id)

    @property
    def stage(self):
        return self.__stages.current

    @property
    def stages(self):
        return self.__stages

    @property
    def proposals(self):
        # todo: return readonly
        return self.__proposals

    @property
    def allowed_users(self):
        # todo: return readonly
        return self.__allowed_users

    # Events

    @property
    def state_changed(self):
        """
        Retrun state changed event.

        Returns:
            Event -- State changed.
        """
        return self.__state_changed

    @property
    def closed(self) -> Event:
        """
        Meeting is closed.

        Returns:
            Event -- Event
        """
        return self.__closed

    @property
    def send_message(self):
        """
        Retrun send event.

        Returns:
            Event -- Send message event.
        """
        return self.__send_message

    @property
    def meeting_id(self):
        """
        Return meeting ID.

        Returns:
            str -- Meeting ID
        """
        return self.__meeting_id

    def command(self, event, *data):
        """
        Command to execute

        Arguments:
            event {str} -- Command.

        Returns:
            obj -- Result of execution.
        """
        return self.__processor.exec(event, *data)

    @property
    def sessions(self):
        """
        Return sessions.

        Returns:
            Sessions -- Sessions.
        """
        return self.__sessions

    # User section

    def find_user(self, id):
        return User.objects.get(pk=id)

    def get_user(self, sid):
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
        allowed_users = self.allowed_users
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
                       self.allowed_users)
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

    # actions

    def close_meeting(self):
        # move all proposals to the next stage
        for proposal in self.proposals:
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

                # meeting is closed
                self.__closed.notify(self)
            except ValueError:
                pass

    def send(self, message, data, to=None):
        self.send_message.notify(message, data, to)

    def full_sync(self):
        serializer = MeetingSerializer()
        meeting_state = serializer.serialize(self)
        self.send_message.notify("full_sync", meeting_state)

    def __on_stage_changed(self, index, stage):
        """
        State of the a stage has been changed.

        Arguments:
            index {int} -- Index of the changed stage.
            stage {MeetingStage} -- Meeting stage.
        """
        # stage changed, serialize it
        serializer = MeetingStageSerializer()
        stage_state = serializer.serialize(stage)

        # send serialized data to all connected
        # clients using all endpoints
        self.state_changed.notify({"index": index, "state": stage_state})

    def __on_sessions_changed(self):
        """
        List of active sessions are changed.
        Update list of online users for clients.
        """
        self.send("meeting_users_online", self.sessions.state)


class QuickBallot():
    """Quick Ballot."""

    def __init__(self):
        """Initializes new instance of a QuickBallot class."""
        self.__result = {}

    def start_new(self):
        """Start a new Quick Ballot."""
        self.__result = {}

    @property
    def results(self):
        """Return results of current ballot."""
        return self.__result

    def vote(self, value):
        """Commit a vote for specified option."""
        if value in self.__result:
            self.__result[value] += 1  # increment count
        else:
            self.__result[value] = 1  # this is a first vote
        return self.results


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
        