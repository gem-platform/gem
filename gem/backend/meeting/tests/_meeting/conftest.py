from pytest import fixture

from gem.db import (User, Role, Proposal, Meeting as MeetingObj, WorkflowType,
                    WorkflowStage)
from gms.app.active_meeting import ActiveMeeting
from gms.meeting.stages import *
from gms.app.context import Context


class DummyMeetingStage(MeetingStage):
    """Dummy meeting stage"""

    def __init__(self, group=None):
        """Initializes new instance of the DummyMeetingStage class."""
        super().__init__(group=group)
        self.on_enter_called = False
        self.on_leave_called = False

    def do_something(self):
        """Do something."""
        self.changed.notify()

    def on_leave(self):
        self.on_leave_called = True

    def on_enter(self):
        self.on_enter_called = True

##


@fixture(name="meeting_obj")
def meeting_obj_fixture(proposal):
    """Meeting with stages."""
    meeting1 = MeetingObj(
        title="Meeting", agenda="Agenda", proposals=[proposal])
    meeting1.save()
    return meeting1


@fixture(name="role")
def role_fixture():
    """Dummy Role"""
    role = Role(name="Tester", priority=99, permissions=['*'])
    role.save()
    return role


@fixture(name="user")
def user_fixture(role):
    """Dummy user"""
    user = User(name="Tester Das", password="pwd", roles=[role])
    user.save()
    return user


@fixture(name="workflow")
def workflow_fixture():
    stage = WorkflowStage(name="General", actions=["ballot"])
    stage.save()
    workflow = WorkflowType(name="General Workflow", stages=[stage])
    workflow.save()
    return workflow


@fixture(name="proposal")
def proposal_fixture(workflow):
    """Proposal."""
    proposal = Proposal(
        title="Proposal 01", index="p01", content="content",
        workflow=workflow, stage=workflow.stages[0])
    proposal.save()
    return proposal


@fixture(name="meeting")
def meeting_fixture(stages):
    """Meeting with stages."""
    meeting = ActiveMeeting()
    for stage in stages:
        meeting.stages.append(stage)
    return meeting


@fixture(name="empty_meeting")
def empty_meeting_fixture():
    """Empty meeting."""
    return ActiveMeeting()


@fixture(name="stages")
def stages_fixture(proposal, acquaintance):
    """Return array of meeting stages to be added to meeting."""
    group1 = StagesGroup(proposal=proposal)

    return [
        AgendaMeetingStage("Some agenda 1", group=group1),
        DummyMeetingStage(group=group1),
        DummyMeetingStage(group=group1),
        CommentsMeetingStage(comments=[], group=group1),
        acquaintance
    ]


@fixture(name="meeting_stages_empty")
def meeting_stages_empty_fixture():
    """Returns dummy meeting stages."""
    return MeetingStages()


@fixture(name="meeting_stages")
def meeting_stages_fixture(stages):
    """Returns dummy meeting stages with several stages added."""
    meeting_stages = MeetingStages()
    for stage in stages:
        meeting_stages.append(stage)
    return meeting_stages


@fixture(name="acquaintance")
def acquaintance_fixture(ballot=None, comments=[]):
    return AcquaintanceMeetingStage(ballot=None, comments=[])