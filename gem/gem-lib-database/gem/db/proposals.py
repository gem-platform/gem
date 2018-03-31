from mongoengine import Document, StringField


class Proposal(Document):
    """
    Proposal document
    """
    title = StringField(required=True)
    index = StringField(required=True)
    content = StringField(required=True)
