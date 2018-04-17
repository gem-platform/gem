from itertools import chain
from mongoengine import (signals, Document, StringField, BooleanField,
                         DictField, ListField, ReferenceField,
                         EmbeddedDocumentField, EmbeddedDocument, DateTimeField)

from gem.db.signals import make_ballot_secret


class GemDocument(Document):
    meta = {
        'abstract': True,
    }
    created = DateTimeField(db_field="_created")
    updated = DateTimeField(db_field="_updated")
    etag = StringField(db_field="_etag")


class Proposal(GemDocument):
    """Proposal document"""
    meta = {'collection': 'proposals'}

    title = StringField(required=True)
    index = StringField(required=True)
    content = StringField(required=True)


class Role(Document):
    """Role"""
    meta = {'collection': 'roles'}

    name = StringField(required=True)
    permissions = ListField()


class User(Document):
    """User"""
    meta = {'collection': 'users'}

    name = StringField(required=True)
    roles = ListField(ReferenceField(Role))
    password = StringField(required=True)

    @property
    def permissions(self):
        permissions = chain.from_iterable([r.permissions for r in self.roles])
        return list(set(permissions))


class BallotRecord(EmbeddedDocument):
    user = ReferenceField(User)
    value = StringField()


class Ballot(Document):
    """Stores ballot data."""
    meta = {'collection': 'ballots'}

    secret = BooleanField()
    votes = ListField(EmbeddedDocumentField(BallotRecord))
    proposal = ReferenceField(Proposal)

    def __init__(self, proposal=None, **data):
        super().__init__(**data)
        self.proposal = proposal

    def set(self, user, value):
        # self.votes[user.id] = value
        record = self.__get(user) or BallotRecord()
        record.user = user
        record.value = value
        if record not in self.votes:
            self.votes.append(record)

    def __get(self, user):
        votes_of_user = list(filter(lambda x: x.user == user, self.votes))
        return votes_of_user[0] if votes_of_user else None


class Comment(Document):
    """Comment"""
    meta = {'collection': 'comments'}

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
    meta = {'collection': 'meetings'}

    title = StringField()
    agenda = StringField()
    proposals = ListField(ReferenceField(Proposal))
    permissions = EmbeddedDocumentField(MeetingPermissions)


# signals
signals.pre_save.connect(make_ballot_secret, sender=Ballot)
