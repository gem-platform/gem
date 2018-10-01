"""Provides function to fill meeting with testing data."""
from bson import ObjectId
from inspect import signature

from gem.db import (Proposal, Ballot, User, Meeting,
                    Comment, Role, MeetingPermission)
from gms.meeting.stages import (
    StagesGroup, AgendaMeetingStage, AcquaintanceMeetingStage,
    BallotMeetingStage, BallotResultsMeetingStage, CommentsMeetingStage,
    DiscussionMeetingStage, FinalMeetingStage
)


def fill_meeting(meeting, meeting_id):
    """Fill specified meeting with test data"""
    # get meeting from database
    db_meeting = Meeting.objects.get(id=ObjectId(meeting_id))

    # add agenda stage
    agenda_stage = AgendaMeetingStage(db_meeting.agenda)
    meeting.stages.append(agenda_stage)

    # create stages for each proposal
    for proposal in db_meeting.proposals:
        add_group(meeting, proposal)

    # add final stage
    meeting.stages.append(FinalMeetingStage())

    # create users
    for user in db_meeting.resolve("meeting.join"):
        meeting.allowed_users.append(user)

    # append users with superuser rights
    superuser_roles = Role.objects(permissions__in=["*"])
    for user in User.objects(roles__in=superuser_roles):
        if user not in meeting.allowed_users:
            meeting.allowed_users.append(user)

    # set time
    meeting.start = db_meeting.start
    meeting.end = db_meeting.end


def add_group(meeting, proposal):
    workflow = proposal.workflow
    cur_stage = proposal.stage
    stage_idx = workflow.stages.index(cur_stage)
    stage_idx = max(0, stage_idx-1) # don't go to negative side
    prev_stage = workflow.stages[stage_idx]
    group = StagesGroup(meeting, proposal=proposal)

    __stages = {
        "acquaintance": __acquaintance_stage,
        "ballot": __ballot_stage,
        "ballot.results": __ballot_results_stage,
        "comments": __comments_stage,
        "discussion": __discussion_stage
    }

    # add meeting stages based on current stage actions
    for action in cur_stage.actions:
        handler = __stages[action.id]
        handler_args = list(signature(handler).parameters)
        handler_params = {
            "group": group, "proposal": proposal, "prev_stage": prev_stage,
            "current_stage": cur_stage, "action": action
        }
        filtered_args = {k: v for k, v in handler_params.items() if k in handler_args}

        stage = __stages[action.id](**filtered_args)
        stage.config = action.config
        meeting.stages.append(stage)

    # add proposal to the meeting
    meeting.proposals.append(proposal)


def __acquaintance_stage(group, prev_stage, action, proposal):
    if action.config.get("commentsDisplayMode", None) == "prev-stage":
        comments = Comment.objects(proposal=proposal, stage=prev_stage)
    else:
        comments = Comment.objects(proposal=proposal)

    ballot = Ballot.objects(proposal=proposal, stage=prev_stage).first()
    return AcquaintanceMeetingStage(ballot, list(comments), group=group)


def __ballot_stage(group, current_stage, proposal):
    ballots = Ballot.objects(proposal=proposal, stage=current_stage)
    ballot = ballots.first() if ballots else Ballot(proposal=proposal, stage=current_stage)
    ballot.save()  # save entity to make it possible to find in another stages (ballot.results)
    return BallotMeetingStage(ballot, group=group)


def __ballot_results_stage(group, current_stage, proposal):
    ballot = Ballot.objects.get(proposal=proposal, stage=current_stage)
    return BallotResultsMeetingStage(ballot, group=group)


def __comments_stage(group, current_stage, proposal):
    comments = Comment.objects(proposal=proposal, stage=current_stage)
    return CommentsMeetingStage(list(comments), group=group)


def __discussion_stage(group):
    return DiscussionMeetingStage(group=group)
