"""Fixtures for unit tests"""
from pytest import fixture

from gms.meeting.stages import (MeetingStages, AgendaMeetingStage, 
                                MeetingStage, FinalMeetingStage)


class DummyMeetingStage(MeetingStage):
    def __init__(self):
        super().__init__(group=None)
        self.on_enter_called = False
        self.on_leave_called = False

    def on_leave(self):
        self.on_leave_called = True

    def on_enter(self):
        self.on_enter_called = True


@fixture(name="meeting_stages_list")
def meeting_stages_list_fixture():
    """Return array of meeting stages to be added to meeting."""
    return [
        AgendaMeetingStage(), FinalMeetingStage(),
        DummyMeetingStage(), DummyMeetingStage()
    ]


@fixture(name="meeting_stages_empty")
def meeting_stages_empty_fixture():
    """Returns dummy meeting stages."""
    return MeetingStages()


@fixture(name="meeting_stages")
def meeting_stages_fixture(meeting_stages_list):
    """Returns dummy meeting stages with several stages added."""
    meeting_stages = MeetingStages()
    for stage in meeting_stages_list:
        meeting_stages.append(stage)
    return meeting_stages
