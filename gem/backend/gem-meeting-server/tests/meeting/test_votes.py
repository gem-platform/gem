import pytest
from gem.db import Proposal, Ballot, Role, User, OpForbidden

from tools import drop_db


def teardown_function():
    drop_db()


def test_user_role_saved(user):
    """User role should be saved."""
    proposal = Proposal()
    ballot = Ballot(proposal=proposal)
    ballot.set(user, "yes")
    assert ballot.votes[0].role == user.roles[0]


def test_right_role_priority():
    """Right role (with maximum priority) should be saved for ballot."""
    proposal = Proposal()
    ballot = Ballot(proposal=proposal)

    role1 = Role()
    role2 = Role()
    role1.priority = 1
    role2.priority = 5

    user = User()
    user.roles.append(role1)
    user.roles.append(role2)

    ballot.set(user, True)
    assert ballot.votes[0].role == role1


def test_unable_to_vote_for_finished_ballot(user):
    """Unable to vote for finished ballot"""
    proposal = Proposal()
    ballot = Ballot(proposal=proposal, finished=True)

    with pytest.raises(OpForbidden, match="Ballot is finished already."):
        ballot.set(user, False)


def test_user_is_not_saved_for_secret_ballot(proposal, user):
    """User is should not be saved for secret ballot."""
    ballot = Ballot(proposal=proposal, secret=True)
    ballot.set(user, "yes")
    ballot.save()

    for vote in ballot.votes:
        assert vote.user is None


def test_user_saved_for_open_ballot(proposal, user):
    """User should be saved for open ballot."""
    ballot = Ballot(proposal=proposal, secret=False)
    ballot.set(user, "yes")
    ballot.save()

    for vote in ballot.votes:
        assert vote.user is user
