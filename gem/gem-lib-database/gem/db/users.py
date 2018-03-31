from mongoengine import Document, StringField


class User(Document):
    """
    User
    """
    name = StringField(required=True)
