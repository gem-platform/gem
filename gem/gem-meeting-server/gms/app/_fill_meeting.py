"""Provides function to fill meeting with testing data."""

import uuid

from gem.db import Proposal, Ballot, User
from gms.meeting.stages import (
    StagesGroup, AgendaMeetingStage, AcquaintanceMeetingStage,
    BallotMeetingStage, BallotResultsMeetingStage, CommentsMeetingStage,
    DiscussionMeetingStage
)


def fill_meeting(meeting):
    """Fill specified meeting with test data"""
    # todo: populate with real data

    meeting.stages.append(AgendaMeetingStage("Some agenda"))
    add_group(meeting, "First proposal")
    add_group(meeting, "Second proposal")

    user1 = User("User 01")
    user2 = User("User 02")
    user1.id = "u01"
    user2.id = "u02"
    meeting.allowed_users.append(user1)
    meeting.allowed_users.append(user2)


def add_group(meeting, proposal_title):
    proposal = Proposal(title=proposal_title)
    proposal.id = uuid.uuid4().hex
    proposal.content = "Content of '{}'".format(proposal_title)

    ballot = Ballot()

    group = StagesGroup(meeting, proposal=proposal)
    meeting.stages.append(AcquaintanceMeetingStage(group=group))
    meeting.stages.append(BallotMeetingStage(ballot, group=group))
    meeting.stages.append(BallotResultsMeetingStage(ballot, group=group))
    meeting.stages.append(CommentsMeetingStage(group=group))
    meeting.stages.append(DiscussionMeetingStage(group=group))
    meeting.proposals.append(proposal)
