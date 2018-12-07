"""Commenting stage of a meeting."""

from gem.db import Comment
from gms.meeting.stages import MeetingStage


class CommentsMeetingStage(MeetingStage):
    """Comments stage of the meeting."""
    __VALID_MARKS = ["+", "-", "i"]

    def __init__(self, comments, group=None):
        """
        Initialize new instance of the CommentsMeetingStage class.

        Arguments:
            comments {list(Comment)} -- Comments.

        Keyword Arguments:
            group {StageGroup} -- Group of the stage. (default: {None})
        """
        super().__init__(group=group)
        self.__comments = comments

    @property
    def comments(self):
        """
        Return comments.

        Returns:
            [Comment] -- List of comments.
        """
        return self.__comments

    def comment(self, user, message, mark, quote=None):
        """
        Add comment using specified user, message and mark.

        Arguments:
            user {User} -- User.
            message {str} -- Message.
            mark {str} -- Mark (+, -, i, etc).
            quote {dict} -- Quotation data.
        """
        # no proposal provided for stage
        if not (self.group and self.group.proposal):
            raise ValueError("No proposal provided for stage")

        # validate mark
        if mark not in self.__VALID_MARKS:
            raise ValueError("Invalid mark")

        # create new comment
        comment = Comment(
            user=user, proposal=self.group.proposal,
            content=message, mark=mark,
            stage=self.group.proposal.stage,
            quote=quote)
        comment.save()

        self.__comments.append(comment)
        self.changed.notify()
