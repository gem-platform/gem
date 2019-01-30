"""Provides function to fill meeting with testing data."""
from inspect import signature
from bson import ObjectId

from gem.db import (Ballot, User, Meeting, Comment, Role, MeetingStageState)
from gms.meeting.stages import (
    StagesGroup, AgendaMeetingStage, AcquaintanceMeetingStage,
    BallotMeetingStage, BallotResultsMeetingStage, CommentsMeetingStage,
    DiscussionMeetingStage, FinalMeetingStage, FeedbackMeetingStage
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
        add_group(db_meeting, meeting, proposal)

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

    # save
    db_meeting.save()

    return db_meeting


def add_group(db_meeting, meeting, proposal):
    workflow = proposal.workflow
    cur_stage = proposal.stage
    stage_idx = workflow.stages.index(cur_stage)
    stage_idx = max(0, stage_idx-1) # don't go to negative side
    prev_stage = workflow.stages[stage_idx]
    group = StagesGroup(meeting, proposal=proposal)
    context = {}

    __stages = {
        "acquaintance": __acquaintance_stage,
        "ballot": __ballot_stage,
        "ballot.results": __ballot_results_stage,
        "comments": __comments_stage,
        "discussion": __discussion_stage,
        "feedback": __feedback_stage
    }

    # add meeting stages based on current stage actions
    for action in cur_stage.actions:
        stage_state = __get_stage_state(db_meeting, proposal, action.id)
        handler = __stages.get(action.id, None)
        if not handler:
            raise Exception("Unknown action type '{}'".format(action.id))

        handler_args = list(signature(handler).parameters)
        handler_params = {
            "group": group, "proposal": proposal, "prev_stage": prev_stage,
            "current_stage": cur_stage, "action": action, "context": context,
            "state": stage_state
        }
        filtered_args = {k: v for k, v in handler_params.items() if k in handler_args}

        stage = __stages[action.id](**filtered_args)
        stage.config = action.config
        meeting.stages.append(stage)

    # add proposal to the meeting
    meeting.proposals.append(proposal)


def __acquaintance_stage(group, prev_stage, action, proposal, state):
    if action.config.get("commentsDisplayMode", None) == "prev-stage":
        comments = Comment.objects(proposal=proposal, stage=prev_stage)
    else:
        comments = Comment.objects(proposal=proposal)

    ballot = Ballot.objects(proposal=proposal, stage=prev_stage).first()
    return AcquaintanceMeetingStage(ballot, list(comments), group=group, state=state)


def __ballot_stage(group, current_stage, proposal, context, state):
    ballots = Ballot.objects(proposal=proposal, stage=current_stage)
    ballot = ballots.first() if ballots else Ballot(proposal=proposal, stage=current_stage)
    context["ballot"] = ballot # save entity to make it possible to find in another stages (ballot.results)
    return BallotMeetingStage(ballot, group=group, state=state)


def __ballot_results_stage(group, context):
    return BallotResultsMeetingStage(context["ballot"], group=group)


def __comments_stage(group, current_stage, proposal):
    comments = Comment.objects(proposal=proposal, stage=current_stage)
    return CommentsMeetingStage(list(comments), group=group)


def __discussion_stage(group):
    return DiscussionMeetingStage(group=group)


def __feedback_stage(group, current_stage, proposal, context, state):
    ballots = Ballot.objects(proposal=proposal, stage=current_stage)
    ballot = ballots.first() if ballots else Ballot(proposal=proposal, stage=current_stage)
    comments = Comment.objects(proposal=proposal, stage=current_stage)

    # save entity to make it possible to find in another stages (ballot.results)
    context["ballot"] = ballot

    return FeedbackMeetingStage(ballot, list(comments), group=group, state=state)


def __get_stage_state(db_meeting, proposal, stage):
    states = list(filter(lambda x: x.proposal == proposal and x.stage == stage, db_meeting.state))

    # no state found, create a new one
    if not states:
        state = MeetingStageState(proposal=proposal, stage=stage)
        db_meeting.state.append(state)
        return state

    # if only one state found
    if len(states) == 1:
        return states[0]

    # many states founf for specified arguments
    raise Exception("Many states for one stage and proposal")
