from mongoengine import (Document, StringField, BooleanField, DictField,
                         ListField, ReferenceField, EmbeddedDocumentField,
                         EmbeddedDocument)


class Proposal(Document):
    """Proposal document"""
    title = StringField(required=True)
    index = StringField(required=True)
    content = StringField(required=True)


class Ballot(Document):
    """Stores ballot data."""
    secret = BooleanField()
    votes = DictField()

    def set(self, user, value):
        self.votes[user.id] = value


class Role(Document):
    """Role"""
    name = StringField(required=True)
    permissions = ListField()


class User(Document):
    """User"""
    name = StringField(required=True)
    roles = ListField(ReferenceField(Role))


class Comment(Document):
    """Comment"""
    user = ReferenceField(User, required=True)
    proposal = ReferenceField(Proposal, required=True)
    content = StringField(required=True)
    mark = StringField(required=True)


class MeetingPermissionType(EmbeddedDocument):
    roles = ListField(ReferenceField(Role))
    users = ListField(ReferenceField(User))

    def all(self):
        result = set()

        for role in self.roles:
            users_with_role = User.objects(roles__in=[role])
            for user in users_with_role:
                result.add(user)

        for user in self.users:
            result.add(user)

        return list(result)


class MeetingPermissions(EmbeddedDocument):
    join = EmbeddedDocumentField(MeetingPermissionType)
    vote = EmbeddedDocumentField(MeetingPermissionType)


class Meeting(Document):
    """Meeting document"""
    title = StringField()
    agenda = StringField()
    proposals = ListField(ReferenceField(Proposal))
    permissions = EmbeddedDocumentField(MeetingPermissions)
