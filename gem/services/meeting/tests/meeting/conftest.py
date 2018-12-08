from pytest import fixture

from gem.db import User, Proposal

from gms.app.active_meeting import ActiveMeeting
from gms.app._fill_meeting import fill_meeting


@fixture(name="meeting")
def meeting_fixture():
    meeting = ActiveMeeting()
    fill_meeting(meeting, "5a5deebeb5385609a9c9face")
    return meeting


@fixture(name="user")
def user_fixture():
    return User.objects.first()


@fixture(name="proposal")
def proposal_fixture():
    return Proposal.objects.first()
