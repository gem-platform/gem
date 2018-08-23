from pytest import raises

from gem.db import Comment
from tools import drop_db

def teardown_function():
    drop_db()


# def test_comment_with_no_proposal(meeting, user):
#     comments_stage = meeting.stages.all[2]
#     with raises(ValueError, match="No proposal provided for comment"):
#         comments_stage.comment(user, "test comment", "+")

def test_comments(meeting, user, proposal):
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
