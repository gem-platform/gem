"""Provides function to fill meeting with testing data."""
from bson import ObjectId

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
    for action in cur_stage.actions:
        stage = None

        if "acquaintance" == action.id:
            if "commentsDisplayMode" in action.config and action.config["commentsDisplayMode"] == "prev-stage":
                comments = Comment.objects(proposal=proposal, stage=prev_stage)
            else:
                comments = Comment.objects(proposal=proposal)
            
            ballot = Ballot.objects(proposal=proposal, stage=prev_stage).first()

            stage = AcquaintanceMeetingStage(ballot, list(comments), group=group)

        if "ballot" == action.id:
            ballots = Ballot.objects(proposal=proposal, stage=cur_stage)
            ballot = ballots[0] if ballots else Ballot(proposal=proposal, stage=cur_stage)

            stage = BallotMeetingStage(ballot, group=group)

        if "ballot.results" == action.id:
            stage = BallotResultsMeetingStage(ballot, group=group)

        if "comments" == action.id:
            comments = Comment.objects(proposal=proposal, stage=cur_stage)
            stage = CommentsMeetingStage(list(comments), group=group)

        if "discussion" == action.id:
            stage = DiscussionMeetingStage(group=group)

        stage.config = action.config
        meeting.stages.append(stage)

    # add proposal to the meeting
    meeting.proposals.append(proposal)