from inspect import getmembers, isfunction

from gem.core import Processor, Event
from gem.db import User

from gms.net.serializers.meeting import MeetingStageSerializer
from gms.net.serializers.meeting import MeetingSerializer
from gms.app._fill_meeting import fill_meeting
from gms.meeting.stages import MeetingStages
from gms.app.sessions import Sessions
from gms.meeting.widgets import QuickBallot, Quorum

import gms.commands as commands

class ActiveMeeting:
    """Active meeting."""

    def __init__(self, meeting_id, intercom):
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
        self.__stages.switched.subscribe(self.__on_stage_switched)
        self.__stages.changed.subscribe(self.__on_stage_changed)

        self.__intercom = intercom
        self.__proposals = []
        self.__allowed_users = []
        self.start = None
        self.end = None
        self.quick_ballot = QuickBallot()
        self.quorum = Quorum(self)

        # events
        self.closed = Event()

        # configure processor:
        # get list of all functions in module
        processor_handlers = getmembers(commands, isfunction)

        # and register them as handler: func_name -> func
        self.__processor = Processor(self)
        self.__processor.register_handlers(processor_handlers)

        if meeting_id is not None:
            self.__meeting_db_obj = fill_meeting(self, meeting_id)

    @property
    def title(self) -> str:
        return self.__meeting_db_obj.title

    @property
    def agenda(self) -> str:
        return self.__meeting_db_obj.agenda

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

    # Properties

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
                self.closed.notify(self)
            except ValueError:
                pass

    def send(self, message, data, to=None):
        self.__intercom.emit(message, data, to)

    def full_sync(self):
        serializer = MeetingSerializer()
        meeting_state = serializer.serialize(self)
        self.__intercom.emit("full_sync", meeting_state)

    def __on_stage_changed(self, index, stage):
        self.__update_stage_data(index, stage, follow=False)

    def __on_stage_switched(self, index, stage):
        self.__update_stage_data(index, stage, follow=True)

    def __on_sessions_changed(self):
        """
        List of active sessions are changed.
        Update list of online users for clients.
        """
        self.__intercom.emit("meeting_users_online", self.sessions.state)

    def __update_stage_data(self, index, stage, follow=False):
        """
        State of the a stage has been changed.

        Arguments:
            index {int} -- Index of the changed stage.
            stage {MeetingStage} -- Meeting stage.
        """
        # stage changed, serialize it
        serializer = MeetingStageSerializer()
        stage_state = serializer.serialize(stage)

        # send serialized data to all connected clients
        self.__intercom.emit(
            "stage_switched" if follow else "stage", \
                {"index": index, "state": stage_state}
            )
