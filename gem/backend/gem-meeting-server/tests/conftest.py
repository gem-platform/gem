from pytest import fixture

from gms.meeting import Meeting
from gms.meeting.stages import MeetingStage, AgendaMeetingStage
from gms.app.context import Context


class DummyMeetingStage(MeetingStage):
    """Dummy meeting stage"""

    def __init__(self):
        """Initializes new instance of the DummyMeetingStage class."""
        super().__init__()

    def do_something(self):
        """Do something."""
        self.changed.notify()


@fixture
def stages():
    """Meeting stages."""
    stage1 = AgendaMeetingStage("Some agenda 1")
    stage2 = DummyMeetingStage()
    return [stage1, stage2]


@fixture
def meeting(stages):
    """Meeting with stages."""
    meeting1 = Meeting(context=Context())
    for stage in stages:
        meeting1.stages.append(stage)
    return meeting1


@fixture
def empty_meeting():
    """Empty meeting."""
    meeting1 = Meeting(context=Context())
    return meeting1
