from gem.db import Comment
from gms.meeting.stages import MeetingStage


class CommentsMeetingStage(MeetingStage):
    """Comments stage of the meeting."""

    def __init__(self, group=None):
        """
        Initialize new instance of the CommentsMeetingStage class.

        Keyword Arguments:
            group {StageGroup} -- Group of the stage. (default: {None})
        """
        super().__init__(group=group)
        self.__comments = []

    @property
    def comments(self):
        """
        Return comments.

        Returns:
            [Comment] -- List of comments.
        """
        return self.__comments

    def comment(self, user, message, mark):
        """
        Add comment using specified user, message and mark.

        Arguments:
            user {User} -- User.
            message {str} -- Message.
            mark {str} -- Mark (+, -, i, etc).
        """
        comment = Comment(user, self.group.proposal)
        comment.content = message
        comment.mark = mark
        self.__comments.append(comment)
        self.changed.notify()

        msg = "comment '{}' accepted from '{}' with mark '{}'"
        print(msg.format(message, user.name, mark))
