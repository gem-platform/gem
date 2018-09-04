from pytest import raises

from gms.meeting.stages import MeetingStages, AgendaMeetingStage


def test_all():
    """All should return all appended stages."""
    meeting_stages = MeetingStages()
    stage1 = AgendaMeetingStage()
    meeting_stages.append(stage1)
    assert meeting_stages.all == [stage1]


def test_current_none():
    """current should return None, index - 0 if no stage added."""
    meeting_stages = MeetingStages()
    assert meeting_stages.current is None
    assert meeting_stages.index == 0


def test_switch_to():
    """Should switch to specified stage."""
    meeting_stages = MeetingStages()

    stage1 = AgendaMeetingStage()
    stage2 = AgendaMeetingStage()
    meeting_stages.append(stage1)
    meeting_stages.append(stage2)

    meeting_stages.switch_to(1)

    assert meeting_stages.current == stage2
    assert meeting_stages.index == 1


def test_switched_event():
    """Switched event should be called."""
    handler_result = None

    meeting_stages = MeetingStages()
    stage1 = AgendaMeetingStage()
    stage2 = AgendaMeetingStage()
    meeting_stages.append(stage1)
    meeting_stages.append(stage2)

    def __handler(index, stage):
        nonlocal handler_result
        handler_result = (index, stage)

    meeting_stages.switched.subscribe(__handler)
    meeting_stages.switch_to(1)

    assert handler_result == (1, stage2)


def test_index_negative():
    meeting_stages = MeetingStages()
    with raises(ValueError, match="Index can not be negative"):
        meeting_stages.switch_to(-1)


def test_index_out_of_bounds():
    meeting_stages = MeetingStages()
    with raises(ValueError, match="Stage index out of bounds"):
        meeting_stages.switch_to(99)


def test_append_same():
    meeting_stages = MeetingStages()
    stage1 = AgendaMeetingStage()
    meeting_stages.append(stage1)
    with raises(Exception, match="Stage already present"):
        meeting_stages.append(stage1)


def test_changed():
    handler_result = None

    meeting_stages = MeetingStages()
    stage1 = AgendaMeetingStage()
    meeting_stages.append(stage1)

    def __handler(index, stage):
        nonlocal handler_result
        handler_result = (index, stage)

    meeting_stages.changed.subscribe(__handler)
    stage1.changed.notify()

    assert handler_result == (0, stage1)
