from pytest import fixture

from gms.meeting import Meeting
from gms.meeting.stages import AgendaMeetingStage
from gms.app.context import Context


@fixture
def stages():
    stage1 = AgendaMeetingStage("Some agenda 1")
    stage2 = AgendaMeetingStage("Some agenda 2")
    return [stage1, stage2]


@fixture
def meeting(stages):
    meeting1 = Meeting(context=Context())
    for stage in stages:
        meeting1.stages.append(stage)
    return meeting1


@fixture
def empty_meeting(stages):
    meeting1 = Meeting(context=Context())
    return meeting1