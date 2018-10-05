from pytest import fixture

from gms.app.active_meetings import ActiveMeetings
from gms.app._fill_meeting import fill_meeting


@fixture(name="meetings")
def meetings():
    return ActiveMeetings()
