import pytest
from gem.db import Proposal, Ballot, Role, User, OpForbidden

from tools import drop_db

def teardown_function():
    drop_db()


def test_user_role_in_votes_persistent():
    proposal = Proposal()
    ballot = Ballot(proposal=proposal)

    role1 = Role()
    role2 = Role()
    role1.priority = 1
    role2.priority = 5

    user = User()
    user.roles.append(role2)

    ballot.set(user, True)
    assert ballot.votes[0].role == role2

    # user already voted, so no role should be changed
    user.roles.append(role1)
    assert ballot.votes[0].role == role2


def test_right_role_priority():
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


def test_unapproved_vote_in_finished_meeting(user):
    proposal = Proposal()
    ballot = Ballot(proposal=proposal, finished=True)

    with pytest.raises(OpForbidden, match="Ballot is finished already."):
        ballot.set(user, False)


def test_userid_is_not_saved_for_secret_ballot(user):
    """User is should not be saved for secret ballot."""
    proposal = Proposal()
    ballot = Ballot(proposal=proposal, secret=True)
    ballot.set(user, True)
    ballot.save()

    for vote in ballot.votes:
        assert vote.user is None
