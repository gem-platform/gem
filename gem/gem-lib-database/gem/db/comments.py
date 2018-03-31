from mongoengine import Document, StringField, ReferenceField


class Comment(Document):
    """Comment"""
    user = ReferenceField("User", required=True)
    proposal = ReferenceField("Proposal", required=True)
    content = StringField(required=True)
    mark = StringField(required=True)
