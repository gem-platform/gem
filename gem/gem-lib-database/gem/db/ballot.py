from mongoengine import Document, BooleanField, DictField


class Ballot(Document):
    """Stores ballot data."""
    secret = BooleanField()
    votes = DictField()

    def set(self, user, value):
        self.votes[user.id] = value
