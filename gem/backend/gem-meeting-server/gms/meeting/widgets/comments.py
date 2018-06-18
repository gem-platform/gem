class CommentsSerializeMixin:
    def comments_serialize(self, stage):
        comments = map(self.__map_comment, stage.comments)
        return list(comments)

    @staticmethod
    def __map_comment(comment):
        return {
            "user": comment.user.name,
            "content": comment.content,
            "mark": comment.mark
        }

