from pytest import fixture

from gem.db import (User, Role, Proposal, Meeting as MeetingObj, WorkflowType,
                    WorkflowStage)
from gms.app.active_meeting import ActiveMeeting
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
def workflow_fixture():
    stage1 = WorkflowStage(name="General", actions=["ballot"])
    stage1.save()
    workflow1 = WorkflowType(name="General Workflow", stages=[stage1])
    workflow1.save()
    return workflow1


@fixture(name="proposal")
def proposal_fixture(workflow):
    """Proposal."""
    proposal1 = Proposal(
        title="Proposal 01", index="p01", content="content",
        workflow=workflow, stage=workflow.stages[0])
    proposal1.save()
    return proposal1


@fixture(name="stages")
def stages_fixture(proposal):
    """Meeting stages."""
    group1 = StagesGroup(proposal=proposal)

    stage1 = AgendaMeetingStage("Some agenda 1", group=group1)
    stage2 = DummyMeetingStage(group=group1)
    stage3 = CommentsMeetingStage(comments=[], group=group1)
    return [stage1, stage2, stage3]


@fixture(name="meeting_obj")
def meeting_obj_fixture(proposal):
    """Meeting with stages."""
    meeting1 = MeetingObj(
        title="Meeting", agenda="Agenda", proposals=[proposal])
    meeting1.save()
    return meeting1


@fixture(name="meeting")
def meeting_fixture(stages):
    """Meeting with stages."""
    meeting1 = ActiveMeeting()
    for stage in stages:
        meeting1.stages.append(stage)
    return meeting1


@fixture(name="empty_meeting")
def empty_meeting_fixture():
    """Empty meeting."""
    return ActiveMeeting()


@fixture(name="user")
def user_fixture():
    """Dummy user"""
    role = Role(name="Tester", priority=99, permissions=['*'])
    role.save()

    user = User(name="Tester Das", password="pwd", roles=[role])
    user.save()

    return user
