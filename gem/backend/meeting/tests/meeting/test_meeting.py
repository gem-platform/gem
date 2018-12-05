from unittest.mock import MagicMock

from pytest import raises

from tools import import_db, drop_db
from gem.db import User, Role, Comment, Ballot, OpForbidden

from gms.meeting.stages import CommentsMeetingStage


def setup_function():
    """Setup tests environment."""
    drop_db()
    import_db("tests/meeting/fixtures/general.json")
    import_db("tests/meeting/fixtures/basic_meeting.json")


def test_smoke(meeting):
    """Check entities was loaded properly."""
    assert meeting.proposals[0].title == "Proposal"
    assert meeting.proposals[0].workflow.name == "General"
    assert meeting.proposals[0].stage.name == "Review"


def test_all_returns_list_of_stages(meeting):
    """'all' property should return list of all stages."""
    all_stages = meeting.stages.all  # get all stages of a meeting
    stages_names = map(lambda x: type(x).__name__, all_stages)

    assert list(stages_names) == [
        "AgendaMeetingStage", "AcquaintanceMeetingStage",
        "CommentsMeetingStage", "BallotMeetingStage",
        "BallotResultsMeetingStage", "FinalMeetingStage"]


def test_switch_to_stage(meeting):
    """Test switching to specified stage."""
    meeting.stages.switch_to(1)
    assert meeting.stages.index == 1
    assert type(meeting.stages.current).__name__ == "AcquaintanceMeetingStage"


def test_switch_to_wrong_stage(meeting):
    """Test switching to wrong stage."""
    with raises(ValueError, match="Stage index out of bounds"):
        meeting.stages.switch_to(99)

    with raises(ValueError, match="Index can not be negative"):
        meeting.stages.switch_to(-1)


def test_switch_event(meeting):
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
    assert switch_handler_data == (1, meeting.stages[1])

    # switch to the same stage, no handler should be called
    switch_handler_data = None
    meeting.stages.switch_to(1)
    assert switch_handler_data is None


def test_stage_changed_event(meeting, user):
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
    meeting.stages[1].set_progress(user, 100)
    assert stages_changed_handler_data == (1, meeting.stages[1])


def test_append_same(meeting):
    """It's not allowed to add same stage twice."""
    with raises(Exception, match="Stage already present"):
        meeting.stages.append(meeting.stages[0])


def test_changed(meeting):
    """Changed event should be risen if any stage has been changed."""
    handler_result = None

    def __handler(index, stage):
        nonlocal handler_result
        handler_result = (index, stage)

    meeting.stages.changed.subscribe(__handler)

    for (index, stage) in enumerate(meeting.stages):
        stage.changed.notify()
        assert handler_result == (index, stage)


def test_on_enter_leave(meeting):
    """on_enter/on_leave handlers should be called on switch."""
    for stage in meeting.stages:
        stage.on_enter = MagicMock()
        stage.on_leave = MagicMock()

    meeting.stages.switch_to(1)
    assert len(meeting.stages[1].on_enter.mock_calls) == 1
    assert not meeting.stages[1].on_leave.mock_calls

    meeting.stages.switch_to(2)
    assert len(meeting.stages[1].on_leave.mock_calls) == 1
    assert len(meeting.stages[2].on_enter.mock_calls) == 1
    assert not meeting.stages[2].on_leave.mock_calls


def test_supersuser_can_join_meeting_anyway(meeting, user):
    """Any user with superuser's ('*') rights can join a meeting."""
    assert user in meeting.allowed_users


###

def test_comment_with_no_proposal(user):
    """Put a comment without proposal should raise an exception,"""
    comments_stage = CommentsMeetingStage(comments=[])
    with raises(ValueError, match="No proposal provided for stage"):
        comments_stage.comment(user, "test comment", "+")


def test_comment(meeting, user, proposal):
    comments_stage = meeting.stages.all[2]
    comments_stage.comment(user, "test comment", "+")

    # comment saved
    assert Comment.objects.count() == 1

    # comment saved properly
    comment = Comment.objects.first()
    assert comment.user == user
    assert comment.mark == "+"
    assert comment.content == "test comment"
    assert comment.proposal == proposal


def test_comment_invalid_mark(meeting, user):
    """Comment with invalid mark should raise exception."""
    comments_stage = meeting.stages.all[2]
    with raises(ValueError, match="Invalid mark"):
        comments_stage.comment(user, "test comment", "InvalidMark")


def test_comment_stage(meeting, user, proposal):
    """Comment shold be saved for the right stage."""
    comments_stage = meeting.stages.all[2]
    comments_stage.comment(user, "comment", "+")

    comment = Comment.objects.first()
    assert comment.stage == proposal.stage

##

def test_user_role_saved(user, proposal):
    """User role should be saved."""
    ballot = Ballot(proposal=proposal, stage=proposal.stage)
    ballot.set(user, "yes")
    assert ballot.votes[0].role == user.roles[0]


def test_right_role_priority(proposal):
    """Right role (with maximum priority) should be saved for ballot."""
    ballot = Ballot(proposal=proposal, stage=proposal.stage)

    role1 = Role()
    role2 = Role()
    role1.priority = 1
    role2.priority = 5

    user = User()
    user.roles.append(role1)
    user.roles.append(role2)

    ballot.set(user, True)
    assert ballot.votes[0].role == role1


def test_unable_to_vote_for_finished_ballot(user, proposal):
    """Unable to vote for finished ballot"""
    ballot = Ballot(proposal=proposal, finished=True, stage=proposal.stage)

    with raises(OpForbidden, match="Ballot is finished already."):
        ballot.set(user, False)


def test_user_is_not_saved_for_secret_ballot(proposal, user):
    """User is should not be saved for secret ballot."""
    ballot = Ballot(proposal=proposal, secret=True, stage=proposal.stage)
    ballot.set(user, "yes")
    ballot.save()

    for vote in ballot.votes:
        assert vote.user is None


def test_user_saved_for_open_ballot(proposal, user):
    """User should be saved for open ballot."""
    ballot = Ballot(proposal=proposal, secret=False, stage=proposal.stage)
    ballot.set(user, "yes")
    ballot.save()

    for vote in ballot.votes:
        assert vote.user is user


def test_ballot_stage(meeting, user, proposal):
    """Ballot should be saved for the right stage."""
    ballot_stage = meeting.stages.switch_to(3)
    ballot_stage.vote(user, "yes")
    meeting.stages.switch_to(4)

    ballot = Ballot.objects.first()
    assert ballot.stage == proposal.stage
    assert len(Ballot.objects.all()) == 1


def test_ballot_is_not_finished(meeting):
    ballot_stage = meeting.stages[3]  # ballot stage
    assert ballot_stage.ballot.finished is not True
