from gem.db.core import Model, Repository, Mapper


class Ballot(Model):
    """Stores ballot data."""

    def __init__(self):
        """Initializes new instance of the Ballot class."""
        super().__init__()
        self.__votes = {}
        self.__secret = False

    @property
    def secret(self):
        return self.__secret

    @secret.setter
    def secret(self, value):
        self.__secret = value

    @property
    def votes(self):
        return self.__votes

    def set(self, user, value):
        self.__votes[user.id] = value


class BallotMapper(Mapper):
    """Converts ballot db data to Ballot model and vice versa."""

    def to_model(self, data):
        ballot = Ballot()
        ballot.id = data.get("_id", None)
        ballot.votes = data.get("votes", None)
        return ballot

    def to_db(self, model):
        return {
            "secret": model.secret,
            "votes": model.votes,
        }


class BallotsRepository(Repository):
    """Ballot repository"""

    def __init__(self, collection):
        """
        Initializes new instance of the BallotRepository class.

        Arguments:
            collection -- Collection to load data from.
        """
        super().__init__(collection, BallotMapper())
