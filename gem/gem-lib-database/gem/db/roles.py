from mongoengine import Document, StringField, ListField


class Role(Document):
    """
    Role
    """
    name = StringField(required=True)
    permissions = ListField()
