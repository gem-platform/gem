from gem.db.core import Model, Repository, Mapper


class Comment(Model):
    """Comment"""

    def __init__(self, user, proposal):
        """
        Initializes new instance of the Comment class.

        Arguments:
            user {User} -- Commenter.
            proposal {Proposal} -- Document to comment.
        """
        super().__init__()
        self.__user = user
        self.__proposal = proposal
        self.__content = None
        self.__mark = None

    @property
    def user(self):
        return self.__user

    @property
    def proposal(self):
        return self.__proposal

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    @property
    def mark(self):
        return self.__mark

    @mark.setter
    def mark(self, value):
        self.__mark = value


class CommentsMapper(Mapper):
    """Converts comment db data to User model and vice versa"""

    def to_model(self, data):
        user = None  # load linked user
        proposal = None  # load linked proposal
        c = Comment(user, proposal)
        c.id = data.get("_id", None)
        c.content = data.get("content", None)
        c.type = data.get("type", None)
        return c

    def to_db(self, model):
        return {
            "user_id": model.user.id,
            "proposal_id": model.proposal.id,
            "content": model.content,
            "mark": model.mark
        }


class CommentsRepository(Repository):
    """Comments repository"""

    def __init__(self, collection):
        """
        Initialize new instance of the CommentsRepository class.

        Arguments:
            collection -- Collection to get data from.
        """
        super().__init__(collection, CommentsMapper())
