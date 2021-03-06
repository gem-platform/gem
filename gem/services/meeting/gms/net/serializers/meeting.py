"""Provide a bunch of serializers."""
from itertools import chain
from gms.meeting.widgets.ballot_results import BallotSerializeMixin
from gms.meeting.widgets.comments import CommentsSerializeMixin


class MeetingSerializer:
    """Meeting model serializer."""

    def __init__(self):
        """Initializes new instance of the MeetingSerializer class."""
        self.__stage_serializer = MeetingStageSerializer()

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

        # collect all the related objects from all the stages
        depends_on = map(self.__stage_serializer.depends_on, meeting.stages.all)
        depends_users = set()
        depends_roles = set()
        for objects in depends_on:
            depends_users |= objects.get("users", set())
            depends_roles |= objects.get("roles", set())

        # convert array of roles to dict keyed by role id:
        roles = chain.from_iterable([u.roles for u in meeting.allowed_users])
        roles = {str(r.id): self.__map_role(r) for r in set(roles) | depends_roles}

        # convert array of users to dict keyed by user id
        users = {str(u.id): self.__map_user(u) for u in set(meeting.allowed_users) | depends_users}

        # quorum
        users_can_change_quorum = list(map(lambda x: str(x.id), meeting.quorum.users_can_change))

        # return list of all stages with theirs current states
        # list of proposals used in current meeting
        return {
            "stages": {
                "list": stages,
                "index": meeting.stages.index,
            },
            "quorum": {
                "value": meeting.quorum.value,
                "users_can_change": users_can_change_quorum
            },
            "proposals": proposals,
            "users": users,
            "roles": roles,
            "start": meeting.start.isoformat(),
            "end": meeting.end.isoformat()
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
            "FinalMeetingStage": FinalMeetingStageSerializer(),
            "FeedbackMeetingStage": FeedbackMeetingStageSerializer()
        }

    def serialize(self, stage):
        stage_type = stage.__class__.__name__
        serializer = self.__serializers.get(stage_type, None)
        if serializer:
            return serializer.serialize(stage)
        raise Exception("No serializer found for '{}' stage".format(stage_type))

    def depends_on(self, stage):
        stage_type = stage.__class__.__name__
        serializer = self.__serializers.get(stage_type, None)
        if serializer and hasattr(serializer, "depends_on"):
            return serializer.depends_on(stage)
        return {}



class AcquaintanceMeetingStageSerializer(BallotSerializeMixin, CommentsSerializeMixin):
    """Acquaintance stage serializer."""

    def serialize(self, stage):
        return {
            "type": "AcquaintanceStage",
            "readingProgress": stage.progress,
            "comments": self.comments_serialize(stage),
            "ballotSummary": self.summary_serialize(stage),
            "proposalId": str(stage.group.proposal.id),
            "config": stage.config
        }

    def depends_on(self, stage):
        users = set(map(lambda x: x.user, stage.comments))
        roles = set(chain.from_iterable(map(lambda x: x.roles, users)))
        return {"users": users, "roles": roles}


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
            "threshold": stage.ballot.threshold,
            "proposalId": str(stage.group.proposal.id),
            "finished": stage.ballot.finished,
            "config": stage.config,
            "isQuorumMet": stage.is_quorum_met
        }

    def depends_on(self, stage):
        users = set(stage.meeting.quorum.users_can_change)
        roles = set(chain.from_iterable(map(lambda x: x.roles, users)))
        return {"users": users, "roles": roles}


class BallotResultsMeetingStageSerializer(BallotSerializeMixin):
    def serialize(self, stage):
        return {
            "type": "BallotResultsStage",
            "summary": self.summary_serialize(stage),
            "proposalId": str(stage.group.proposal.id),
            "config": stage.config
        }

    def depends_on(self, stage):
        users = set(map(lambda x: x.user, stage.ballot.votes))
        roles = set(map(lambda x: x.role, stage.ballot.votes))
        return {"users": users, "roles": roles}



class CommentsMeetingStageSerializer(CommentsSerializeMixin):
    def serialize(self, stage):
        return {
            "type": "CommentsStage",
            "comments": self.comments_serialize(stage),
            "proposalId": str(stage.group.proposal.id),
            "config": stage.config
        }

    def depends_on(self, stage):
        users = set(map(lambda x: x.user, stage.comments))
        roles = set(chain.from_iterable(map(lambda x: x.roles, users)))
        return {"users": users, "roles": roles}


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


class FeedbackMeetingStageSerializer:
    def __init__(self):
        self.__acquaintance = AcquaintanceMeetingStageSerializer()
        self.__ballot = BallotMeetingStageSerializer()
        self.__comments = CommentsMeetingStageSerializer()

    def serialize(self, stage):
        a = self.__acquaintance.serialize(stage)
        b = self.__ballot.serialize(stage)
        c = self.__comments.serialize(stage)
        return {**a, **b, **c, "type": "FeedbackStage"}
