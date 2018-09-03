from pytest import raises

from gms.meeting.stages import AgendaMeetingStage
from gms.app.context import Context
from gms.app._fill_meeting import fill_meeting

from tools import drop_db


def teardown_function():
    drop_db()


def test_supersuser_can_join_meeting_anyway(meeting, meeting_obj, user):
    """Any user with superuser's ('*') rights can join a meeting."""
    fill_meeting(meeting, meeting_obj.id)
    assert user in meeting.allowed_users
