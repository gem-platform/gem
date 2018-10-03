class CommentsSerializeMixin:
    def comments_serialize(self, stage):
        comments = map(self.__map_comment, stage.comments)
        return list(comments)

    def __map_comment(self, comment):
        result = {
            "_id": str(comment.id),
            "user_id": str(comment.user.id),
            "content": comment.content,
            "mark": comment.mark,
        }

        if comment.quote:
            result["quote"] = {
                "text": comment.quote.text
            }

        return result
