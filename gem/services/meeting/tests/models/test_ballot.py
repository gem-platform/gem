from pytest import raises

from tools import import_db, drop_db
from gem.db import User, Ballot, Role

from gms.meeting.stages import CommentsMeetingStage


def setup_function():
    """Setup tests environment."""
    drop_db()
    import_db("tests/models/fixtures/ballot.json")


def vote(ballot, value, count):
    role = Role.objects.get(pk="5b8ab052df6e3a05bb720fed")

    for i in range(count):
        user = User(name="user " + str(i) + " " + value, roles=[role], password="123")
        user.save()
        ballot.set(user, value)


def test_empty():
    ballot = Ballot.objects.get(pk="5b8ab052df6e3a05bb720fed")
    ballot.threshold = .5
    assert ballot.result is None


def test_majority():
    ballot = Ballot.objects.get(pk="5b8ab052df6e3a05bb720fed")
    ballot.threshold = .5

    vote(ballot, "yes", 5)
    vote(ballot, "no", 4)
    ballot.save()

    assert ballot.result == "pass"


def test_unanimous():
    ballot = Ballot.objects.get(pk="5b8ab052df6e3a05bb720fed")
    ballot.threshold = 1

    vote(ballot, "yes", 5)
    ballot.save()

    assert ballot.result == "pass"


def test_unanimous_fail():
    ballot = Ballot.objects.get(pk="5b8ab052df6e3a05bb720fed")
    ballot.threshold = 1

    vote(ballot, "yes", 5)
    vote(ballot, "no", 1)
    ballot.save()

    assert ballot.result == "fail"


def test_tie():
    ballot = Ballot.objects.get(pk="5b8ab052df6e3a05bb720fed")
    ballot.threshold = .5

    vote(ballot, "yes", 5)
    vote(ballot, "no", 5)
    ballot.save()

    assert ballot.result == "tie"


def test_tie_unanimous_fail():
    ballot = Ballot.objects.get(pk="5b8ab052df6e3a05bb720fed")
    ballot.threshold = 1

    vote(ballot, "yes", 5)
    vote(ballot, "no", 5)
    ballot.save()

    assert ballot.result == "fail" # no tie for unanimous
