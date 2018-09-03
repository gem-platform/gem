"""Provides function to fill meeting with testing data."""
import os
from bson import ObjectId
from mongoengine import connect

from gem.db import (Proposal, Ballot, User, Meeting,
                    Comment, Role, MeetingPermission)
from gms.meeting.stages import (
    StagesGroup, AgendaMeetingStage, AcquaintanceMeetingStage,
    BallotMeetingStage, BallotResultsMeetingStage, CommentsMeetingStage,
    DiscussionMeetingStage, FinalMeetingStage
)


def fill_meeting(meeting, meeting_id):
    """Fill specified meeting with test data"""
    db_host = os.environ.get('DB_HOST', "localhost")
    db_username = os.environ.get('MONGO_USERNAME')
    db_password = os.environ.get('MONGO_PASSWORD')
    db_auth_source = os.environ.get('MONGO_AUTH_SOURCE')
    db_auth_mechanism = os.environ.get('MONGO_AUTH_MECHANISM')

    connect("gem",
            host=db_host, username=db_username, password=db_password,
            authentication_source=db_auth_source,
            authentication_mechanism=db_auth_mechanism)

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
    stage = proposal.stage

    ballots = Ballot.objects(proposal=proposal)
    ballot = ballots[0] if ballots else Ballot(proposal=proposal)

    comments = list(Comment.objects(proposal=proposal))

    group = StagesGroup(meeting, proposal=proposal)
    if "acquaintance" in stage.actions:
        meeting.stages.append(AcquaintanceMeetingStage(ballot, comments, group=group))

    if "ballot" in stage.actions:
        meeting.stages.append(BallotMeetingStage(ballot, group=group))

    if "ballot.results" in stage.actions:
        meeting.stages.append(BallotResultsMeetingStage(ballot, group=group))

    if "comments" in stage.actions:
        meeting.stages.append(CommentsMeetingStage(comments, group=group))

    if "discussion" in stage.actions:
        meeting.stages.append(DiscussionMeetingStage(group=group))

    meeting.proposals.append(proposal)
