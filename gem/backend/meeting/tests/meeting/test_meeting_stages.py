"""Unit tests for MeetingStage class."""

from pytest import raises


def test_all(meeting_stages, stages):
    """All should return all appended stages."""
    assert meeting_stages.all == stages


def test_current_none(meeting_stages_empty):
    """current should return None, index - 0 if no stage added."""
    assert meeting_stages_empty.current is None
    assert meeting_stages_empty.index == 0


def test_switch_to(meeting_stages, stages):
    """Should switch to specified stage."""
    index_to_switch = 1
    meeting_stages.switch_to(index_to_switch)

    assert meeting_stages.current == stages[index_to_switch]
    assert meeting_stages.index == index_to_switch


def test_switched_event(meeting_stages, stages):
    """Switched event should be called."""
    handler_result = None
    index_to_switch = 1

    def __handler(index, stage):
        nonlocal handler_result
        handler_result = (index, stage)

    meeting_stages.switched.subscribe(__handler)
    meeting_stages.switch_to(index_to_switch)

    assert handler_result == \
        (index_to_switch, stages[index_to_switch])


def test_index_negative(meeting_stages):
    """Index should not be negative."""
    with raises(ValueError, match="Index can not be negative"):
        meeting_stages.switch_to(-1)


def test_index_out_of_bounds(meeting_stages):
    """Index should not be greater than count of stages added."""
    with raises(ValueError, match="Stage index out of bounds"):
        meeting_stages.switch_to(99)


def test_append_same(meeting_stages, stages):
    """It's not allowed to add same stage twice."""
    with raises(Exception, match="Stage already present"):
        meeting_stages.append(stages[0])


def test_changed(meeting_stages, stages):
    """Changed event should be risen if any stage has been changed."""
    handler_result = None

    def __handler(index, stage):
        nonlocal handler_result
        handler_result = (index, stage)

    meeting_stages.changed.subscribe(__handler)

    for (index, stage) in enumerate(stages):
        stage.changed.notify()
        assert handler_result == (index, stage)


def test_on_enter_leave(meeting_stages, stages):
    """on_enter/on_leave handlers should be called on switch."""
    meeting_stages.switch_to(1)
    assert stages[1].on_enter_called is True
    assert stages[1].on_leave_called is False

    meeting_stages.switch_to(2)
    assert stages[1].on_leave_called is True
    assert stages[2].on_enter_called is True
    assert stages[2].on_leave_called is False
