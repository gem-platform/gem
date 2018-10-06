from bson import ObjectId
from pytest import fixture
from munch import Munch
from tools import import_db

from gms.app.active_meetings import ActiveMeetings


class TestSession:
    def __init__(self, api, name):
        self.api = api
        self.name = name

    def __getattr__(self, attr):
        def handler(**data):
            args = data.copy()

            # convert ObjectId to str automatically
            for name, value in args.items():
                if isinstance(value, ObjectId):
                    args[name] = str(value)

            # execute command and return result
            res = self.api.command(attr, self.name, args)
            return Munch(res) if res else None

        return handler

@fixture(name="db")
def db_fixture():
    return import_db("tests/integrational/fixtures/general.json")

@fixture(name="meetings")
def meetings_fixture():
    return ActiveMeetings()


@fixture(name="session")
def session_fixture(meetings):
    return TestSession(meetings, "session01")


@fixture(name="session2")
def session2_fixture(meetings):
    return TestSession(meetings, "session02")
