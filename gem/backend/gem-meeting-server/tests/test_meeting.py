from gms.meeting import Meeting
from gms.meeting.stages import AgendaMeetingStage
from gms.app.context import Context


def test_stage_to_stage():
    """Test switching to specified stage."""
    stage1 = AgendaMeetingStage("Some agenda 1")
    stage2 = AgendaMeetingStage("Some agenda 2")

    meeting = Meeting(context=Context())
    meeting.stages.append(stage1)
    meeting.stages.append(stage2)

    meeting.stages.switch_to(1)
    assert meeting.stages.index == 1
    assert meeting.stages.current == stage2
