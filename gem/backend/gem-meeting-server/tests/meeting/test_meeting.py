from pytest import raises

from gms.meeting import Meeting
from gms.meeting.stages import AgendaMeetingStage
from gms.app.context import Context

from tools import drop_db

def teardown_function():
    drop_db()


def test_all_returns_list_of_stages(meeting, stages):
    """'all' property should return list of all stages."""
    assert meeting.stages.all == stages


def test_current_stage(empty_meeting, stages):
    """'current' property should return current stage or None if
        no stages added."""
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
    with raises(ValueError, match="Stage index out of bounds"):
        meeting.stages.switch_to(99)

    with raises(ValueError, match="Index can not be negative"):
        meeting.stages.switch_to(-1)


def test_switch_event(meeting, stages):
    """'switch' event should be called."""
    switch_handler_data = None

    def switch_event_handler(index, stage):
        """switch event handler"""
        nonlocal switch_handler_data
        switch_handler_data = (index, stage)

    # switch to new stage
    meeting.stages.switched.subscribe(switch_event_handler)
    meeting.stages.switch_to(1)
    assert switch_handler_data is not None
    assert switch_handler_data == (1, stages[1])

    # switch to the same stage, no handler should be called
    switch_handler_data = None
    meeting.stages.switch_to(1)
    assert switch_handler_data is None


def test_stage_changed_event(meeting, stages):
    """'changed' event should be called on stage change."""
    stages_changed_handler_data = None

    # changes handler
    def on_stages_changed(index, stage):
        """meeting changed event handler"""
        nonlocal stages_changed_handler_data
        stages_changed_handler_data = (index, stage)

    # subscribe for changes
    meeting.stages.changed.subscribe(on_stages_changed)

    # provide some action
    stages[1].do_something()
    assert stages_changed_handler_data == (1, stages[1])
