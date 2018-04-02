"""Provides function to fill meeting with testing data."""
import os
from mongoengine import connect

from gem.db import Proposal, Ballot, User, Meeting
from gms.meeting.stages import (
    StagesGroup, AgendaMeetingStage, AcquaintanceMeetingStage,
    BallotMeetingStage, BallotResultsMeetingStage, CommentsMeetingStage,
    DiscussionMeetingStage
)


def fill_meeting(meeting):
    """Fill specified meeting with test data"""
    # todo: populate with real data
    db_host = os.environ.get('DB_HOST', "localhost")

    connect("test", host=db_host)
    db_meeting = Meeting.objects[0]

    # add agenda stage
    agenda_stage = AgendaMeetingStage(db_meeting.agenda)
    meeting.stages.append(agenda_stage)

    # create stages for each proposal
    for proposal in db_meeting.proposals:
        add_group(meeting, proposal)

    # create users
    for user in db_meeting.permissions.join.all():
        meeting.allowed_users.append(user)


def add_group(meeting, proposal):
    ballot = Ballot()

    group = StagesGroup(meeting, proposal=proposal)
    meeting.stages.append(AcquaintanceMeetingStage(group=group))
    meeting.stages.append(BallotMeetingStage(ballot, group=group))
    meeting.stages.append(BallotResultsMeetingStage(ballot, group=group))
    meeting.stages.append(CommentsMeetingStage(group=group))
    meeting.stages.append(DiscussionMeetingStage(group=group))
    meeting.proposals.append(proposal)
