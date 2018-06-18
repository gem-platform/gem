"""Provides function to fill meeting with testing data."""
import os
from bson import ObjectId
from mongoengine import connect

from gem.db import (Proposal, Ballot, User, Meeting,
                    Comment, Role, MeetingPermission)
from gms.meeting.stages import (
    StagesGroup, AgendaMeetingStage, AcquaintanceMeetingStage,
    BallotMeetingStage, BallotResultsMeetingStage, CommentsMeetingStage,
    DiscussionMeetingStage
)


def fill_meeting(meeting, meeting_id):
    """Fill specified meeting with test data"""
    db_host = os.environ.get('DB_HOST', "localhost")

    connect("test", host=db_host)
    db_meeting = Meeting.objects.get(id=ObjectId(meeting_id))
    # Meeting.objects[0] if len(Meeting.objects) > 0 else init_db()

    # add agenda stage
    agenda_stage = AgendaMeetingStage(db_meeting.agenda)
    meeting.stages.append(agenda_stage)

    # create stages for each proposal
    for proposal in db_meeting.proposals:
        add_group(meeting, proposal)

    # create users
    for user in db_meeting.resolve("meeting.join"):
        meeting.allowed_users.append(user)

    #
    meeting.start = db_meeting.start
    meeting.end = db_meeting.end


def add_group(meeting, proposal):
    ballots = Ballot.objects(proposal=proposal)
    ballot = ballots[0] if ballots else Ballot(proposal=proposal)

    comments = list(Comment.objects(proposal=proposal))

    group = StagesGroup(meeting, proposal=proposal)
    meeting.stages.append(AcquaintanceMeetingStage(group=group))
    meeting.stages.append(BallotMeetingStage(ballot, group=group))
    meeting.stages.append(BallotResultsMeetingStage(ballot, group=group))
    meeting.stages.append(CommentsMeetingStage(comments, group=group))
    meeting.stages.append(DiscussionMeetingStage(group=group))
    meeting.proposals.append(proposal)


def init_db():
    prop1 = Proposal()
    prop1.title = "First Proposal"
    prop1.content = "Content of proposal"
    prop1.index = "P001"

    role1 = Role()
    role1.name = "Tester"
    role1.permissions = ["*", "vote", "comment", "discuss"]

    user1 = User()
    user1.name = "Tester das"
    user1.roles.append(role1)
    user1.password = "tester"

    perm1 = MeetingPermission()
    perm1.name = "meeting.join"
    perm1.role = role1
    perm1.user = user1

    meet1 = Meeting()
    meet1.title = "AGM 2018"
    meet1.agenda = "Agenda of testing meeting"
    meet1.proposals.append(prop1)
    meet1.permissions.append(perm1)

    prop1.save()
    role1.save()
    user1.save()
    meet1.save()

    return meet1
