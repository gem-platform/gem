from pytest import raises, fixture

from gms.meeting import Meeting
from gms.meeting.stages import AgendaMeetingStage
from gms.app.context import Context


def test_all_returns_list_of_stages(meeting, stages):
    """'all' property should return list of all stages."""
    assert meeting.stages.all == stages


def test_current_stage(empty_meeting, stages):
    """'current' property should return current stage or None if no stages added."""
    assert empty_meeting.stages.current is None
    empty_meeting.stages.append(stages[0])
    assert empty_meeting.stages.current == stages[0]


def test_switch_to_stage(meeting, stages):
    """Test switching to specified stage."""
    meeting.stages.switch_to(1)
    assert meeting.stages.index == 1
    assert meeting.stages.current == stages[1]


def test_switch_to_wrong_stage(meeting):
    """Test switching to wrong stage."""
    with raises(IndexError, match="Stage index out of bounds"):
        meeting.stages.switch_to(2)

    with raises(ValueError, match="Index can not be negative"):
        meeting.stages.switch_to(-1)


def test_switch_event(meeting, stages):
    """Switch event should be called."""
    switch_handler_data = None

    def switch_event_handler(index, stage):
        """switch event handler"""
        nonlocal switch_handler_data
        switch_handler_data = (index, stage)

    # switch to new stage
    meeting.stages.switch.subscribe(switch_event_handler)
    meeting.stages.switch_to(1)
    assert switch_handler_data is not None
    assert switch_handler_data == (1, stages[1])

    # switch to the same stage, no handler should be called
    switch_handler_data = None
    meeting.stages.switch_to(1)
    assert switch_handler_data is None
