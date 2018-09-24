"""Provide a bunch of serializers."""
from itertools import chain
from gms.meeting.widgets.ballot_results import BallotSerializeMixin
from gms.meeting.widgets.comments import CommentsSerializeMixin

class MeetingSerializer:
    """Meeting model serializer."""

    def __init__(self):
        """Initializes new instance of the MeetingSerializer class."""
        self.__stage_serializer = MeetingStageSerializer()
        # todo: proposal serializer
        # todo: user serializer

    def serialize(self, meeting):
        """
        Serialize meeting into dict.

        Sends all data required for client-side to minimize request to load
        additional data.

        Arguments:
            meeting {Meeting} -- Meeting to serialize.

        Returns:
            dict -- dict representation of specified meeting.
        """
        # serializes stages to dicts and converts array [stage1, stage2, ...]
        # into dictionary {0: stage1, 1: stage2, ...}
        # reason: vuex does not support reactivity for arrays
        stages = map(self.__stage_serializer.serialize, meeting.stages.all)
        stages = {k: v for k, v in enumerate(stages)}

        # convert array of proposals to dict keyed by proposal id
        # [proposal1, proposal2] -> { proposal1.id: proposal, ...}
        # reason: it's easy to access by id on client
        proposals = {str(p.id): p for p in meeting.proposals}
        proposals = {k: self.__map_proposal(v) for k, v in proposals.items()}

        # convert array of users to dict keyed by user id
        users = {str(u.id): self.__map_user(u) for u in meeting.allowed_users}

        # convert array of roles to dict keyed by role id:
        roles = chain.from_iterable([u.roles for u in meeting.allowed_users])
        roles = {str(r.id): self.__map_role(r) for r in roles}

        # return list of all stages with theirs current states
        # list of proposals used in current meeting
        return {
            "stages": {
                "list": stages,
                "index": meeting.stages.index,
            },
            "proposals": proposals,
            "users": users,
            "roles": roles,
            "start": meeting.start.isoformat(),
            "end": meeting.end.isoformat()
            # todo: list of users allowed to present at meeting
            #       including their meta (roles, permissions)
            # todo: list of online users
        }

    def __map_proposal(self, proposal):
        #  ! todo: how serialize models right way?
        #  ! todo: extract to ProposalSerializer
        return {
            "title": proposal.title,
            "content": proposal.content
        }

    def __map_user(self, user):
        return {
            "id": str(user.id),
            "name": user.name,
            "roles": [str(r.id) for r in user.roles],
            "permissions": user.permissions
        }

    def __map_role(self, role):
        return {
            "name": role.name,
            "permissions": role.permissions
        }


class MeetingStageSerializer:
    """Meeting stage serializer."""

    def __init__(self):
        """Initialize new instance of the MeetingStageSerializer class."""
        self.__serializers = {
            "AgendaMeetingStage": AgendaMeetingStageSerializer(),
            "AcquaintanceMeetingStage": AcquaintanceMeetingStageSerializer(),
            "BallotMeetingStage": BallotMeetingStageSerializer(),
            "BallotResultsMeetingStage": BallotResultsMeetingStageSerializer(),
            "CommentsMeetingStage": CommentsMeetingStageSerializer(),
            "DiscussionMeetingStage": DiscussionMeetingStageSerializer(),
            "FinalMeetingStage": FinalMeetingStageSerializer()
        }

    def serialize(self, stage):
        stage_type = stage.__class__.__name__
        serializer = self.__serializers.get(stage_type, None)
        if serializer:
            return serializer.serialize(stage)
        return None


class AcquaintanceMeetingStageSerializer(BallotSerializeMixin, CommentsSerializeMixin):
    """Acquaintance stage serializer."""

    def serialize(self, stage):
        return {
            "type": "AcquaintanceStage",
            "progress": stage.progress,
            "comments": self.comments_serialize(stage),
            "ballotSummary": self.summary_serialize(stage),
            "proposalId": str(stage.group.proposal.id),
            "config": stage.config
        }


class AgendaMeetingStageSerializer:
    def serialize(self, stage):
        return {
            "type": "AgendaStage",
            "content": stage.content
        }


class BallotMeetingStageSerializer(BallotSerializeMixin):
    def serialize(self, stage):
        return {
            "type": "BallotStage",
            "progress": self.progress(stage),
            "secret": stage.ballot.secret,
            "proposalId": str(stage.group.proposal.id),
            "config": stage.config
        }


class BallotResultsMeetingStageSerializer(BallotSerializeMixin):
    def serialize(self, stage):
        return {
            "type": "BallotResultsStage",
            "votes": self.votes_serialize(stage),
            "summary": self.summary_serialize(stage),
            "proposalId": str(stage.group.proposal.id),
            "config": stage.config
        }



class CommentsMeetingStageSerializer(CommentsSerializeMixin):
    def serialize(self, stage):
        return {
            "type": "CommentsStage",
            "comments": self.comments_serialize(stage),
            "proposalId": str(stage.group.proposal.id),
            "config": stage.config
        }


class DiscussionMeetingStageSerializer:
    def serialize(self, stage):
        # get users id only. client already have all users data
        # sent at handshake stage
        user_ids = map(lambda x: str(x.id), stage.queue)
        speaker_id = stage.speaker.id if stage.speaker else None

        return {
            "type": "DiscussionStage",
            "queue": list(user_ids),
            "speaker": str(speaker_id),
            "proposalId": str(stage.group.proposal.id),
            "config": stage.config
        }


class FinalMeetingStageSerializer:
    def serialize(self, stage):
        return {
            "type": "FinalStage",
        }
