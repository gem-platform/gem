import pytest
import sys

sys.path.append('.')
sys.path.append("../gem-server-common")

from gem.db import *

from gms.meeting import Meeting
from gms.meeting.stages import *
from gms.app.context import Context
from gms.app._fill_meeting import add_group


def test_user_role_in_votes_persistent():
    meeting = Meeting(context=Context())
    
    proposal = Proposal()
    ballot = Ballot(proposal = proposal)
    
    role1 = Role()   
    role2 = Role()
    
    user = User()
    user.roles.append(role2)

    ballot.set(user, True)
    assert(len(ballot.votes[0].roles) == 1)
    assert(ballot.votes[0].roles[0] == role2)
    
    user.roles.append(role1)
    assert(len(ballot.votes[0].roles) == 1)
    assert(ballot.votes[0].roles[0] == role2)

    ballot.set(user, False)
    assert(len(ballot.votes[0].roles) == 2)

    user.roles.pop()
    assert(len(ballot.votes[0].roles) == 2)


def test_unapprove_vote_in_finished_meeting():
    meeting = Meeting(context=Context())
    
    proposal = Proposal()
    ballot = Ballot(proposal = proposal)
    ballot.finished = True

    user = User()
    with pytest.raises(OpForbidden, match="Ballot is finished already."):
        ballot.set(user, False)
    
