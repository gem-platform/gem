from itertools import chain
from mongoengine import (signals, Document, StringField, BooleanField,
                         DictField, ListField, ReferenceField,
                         EmbeddedDocumentField, EmbeddedDocument,
                         DateTimeField, GenericReferenceField,
                         EmbeddedDocumentListField)

from gem.db.signals import finalize_ballot


class OpForbidden(Exception):
    pass

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
    stage = StringField()


class Law(GemDocument):
    """Law"""
    meta = {'collection': 'laws'}

    title = StringField(required=True)
    index = StringField(required=True)
    content = StringField(required=True)


class Role(GemDocument):
    """Role"""
    meta = {'collection': 'roles'}

    name = StringField(required=True)
    permissions = ListField()


class User(GemDocument):
    """User"""
    meta = {'collection': 'users'}

    name = StringField(required=True)
    roles = ListField(ReferenceField(Role))
    password = StringField(required=True)

    @property
    def permissions(self):
        permissions = chain.from_iterable([r.permissions for r in self.roles])
        return list(set(permissions))

    def have_permission(self, permission):
        return (permission in self.permissions) or ("*" in self.permissions)


class BallotRecord(EmbeddedDocument):
    user = ReferenceField(User)
    value = StringField()
    roles = ListField(ReferenceField(Role))


class Ballot(Document):
    """Stores ballot data."""
    meta = {'collection': 'ballots'}

    secret = BooleanField()
    votes = ListField(EmbeddedDocumentField(BallotRecord))
    proposal = ReferenceField(Proposal)
    finished = BooleanField()

    def __init__(self, proposal=None, **data):
        super().__init__(**data)
        self.proposal = proposal

    def set(self, user, value):
        if self.finished:
            raise OpForbidden("Ballot is finished already.")
        record = self.__get(user) or BallotRecord()
        record.user = user
        record.value = value
        record.roles = user.roles.copy()
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


class MeetingPermission(EmbeddedDocument):
    scope = StringField()
    user = ReferenceField(User, required=False)
    role = ReferenceField(Role, required=False)


class Meeting(GemDocument):
    """Meeting document"""
    meta = {'collection': 'meetings'}

    title = StringField()
    agenda = StringField()
    proposals = ListField(ReferenceField(Proposal))
    permissions = EmbeddedDocumentListField(MeetingPermission)
    start = DateTimeField()
    end = DateTimeField()

    def resolve(self, permission):
        result = set()
        permissions = filter(lambda x: x.scope == permission, self.permissions)

        for permission in list(permissions):
            if permission.role:
                users_with_role = User.objects(roles__in=[permission.role])
                for user in users_with_role:
                    result.add(user)
            elif permission.user:
                result.add(permission.user)

        return list(result)


# Zonal Assignments


class Official(Document):
    meta = {'collection': 'officials'}
    name = StringField(required=True)
    form_of_address = StringField(db_field="formOfAddress", required=True)
    email = StringField(db_field="email")
    appendage = StringField()
    secretary = BooleanField()
    gbc = BooleanField()

    def formal_name(self):
        formats = {
            "P": {"prefix": "", "postfix": " Das"},
            "S": {"prefix": "", "postfix": " Svami"},
            "G": {"prefix": "", "postfix": " Goswami"},
            "D": {"prefix": "", "postfix": " Das Goswami"},
            "B": {"prefix": "Bhakta ", "postfix": ""},
            "M": {"prefix": "", "postfix": " Devi Dasi"},
            "N": {"prefix": "", "postfix": ""},
        }
        name_format = formats.get(self.form_of_address, None)
        if not name_format:
            return self.name

        return "{}{}{}{}".format(
            name_format["prefix"], self.name, name_format["postfix"],
            " (" + self.appendage + ")" if self.appendage else "")

    def __lt__(self, other):
        return self.name < other.name


class Zone(Document):
    meta = {'collection': 'zones'}
    name = StringField(required=True)
    parent = ReferenceField("Zone")
    officials = ListField(ReferenceField(Official))

    @property
    def children(self):
        return Zone.objects(parent=self)

    def __lt__(self, other):
        return self.name < other.name


# signals
signals.pre_save.connect(finalize_ballot, sender=Ballot)
