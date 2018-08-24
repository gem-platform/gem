from pytest import raises

from gem.db import Comment
from tools import drop_db
from gms.meeting.stages import CommentsMeetingStage


def teardown_function():
    """Teardown test."""
    drop_db()


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
