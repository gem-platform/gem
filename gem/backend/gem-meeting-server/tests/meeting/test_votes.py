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


def test_unapproved_vote_in_finished_meeting():
    proposal = Proposal()
    ballot = Ballot(proposal=proposal)
    ballot.finished = True

    user = User()
    with pytest.raises(OpForbidden, match="Ballot is finished already."):
        ballot.set(user, False)
