from pytest import fixture

from gem.db import User, Role, Proposal, Meeting as MeetingObj, WorkflowType, WorkflowStage
from gms.meeting import Meeting
from gms.meeting.stages import (MeetingStage, AgendaMeetingStage,
                                CommentsMeetingStage, StagesGroup)
from gms.app.context import Context


class DummyMeetingStage(MeetingStage):
    """Dummy meeting stage"""

    def __init__(self, group=None):
        """Initializes new instance of the DummyMeetingStage class."""
        super().__init__(group=group)

    def do_something(self):
        """Do something."""
        self.changed.notify()


@fixture(name="workflow")
def fixture_workflow():
    stage1 = WorkflowStage(name="General", actions=["ballot"])
    stage1.save()
    workflow1 = WorkflowType(name="General Workflow", stages=[stage1])
    workflow1.save()
    return workflow1


@fixture(name="proposal")
def fixture_proposal(workflow):
    """Proposal."""
    proposal1 = Proposal(
        title="Proposal 01", index="p01", content="content",
        workflow=workflow, stage=workflow.stages[0])
    proposal1.save()
    return proposal1


@fixture(name="stages")
def fixture_stages(proposal):
    """Meeting stages."""
    group1 = StagesGroup(proposal=proposal)

    stage1 = AgendaMeetingStage("Some agenda 1", group=group1)
    stage2 = DummyMeetingStage(group=group1)
    stage3 = CommentsMeetingStage(comments=[], group=group1)
    return [stage1, stage2, stage3]


@fixture(name="meeting_obj")
def fixture_meeting_obj(proposal):
    """Meeting with stages."""
    meeting1 = MeetingObj(
        title="Meeting", agenda="Agenda", proposals=[proposal])
    meeting1.save()
    return meeting1

@fixture(name="meeting")
def fixture_meeting(stages):
    """Meeting with stages."""
    meeting1 = Meeting(context=Context())
    for stage in stages:
        meeting1.stages.append(stage)
    return meeting1


@fixture(name="empty_meeting")
def fixture_empty_meeting():
    """Empty meeting."""
    meeting1 = Meeting(context=Context())
    return meeting1


@fixture(name="user")
def fixture_user():
    """Dummy user"""
    role = Role(name="Tester", priority=99, permissions=['*'])
    role.save()

    user = User(name="Tester Das", password="pwd", roles=[role])
    user.save()

    return user
