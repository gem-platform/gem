from tools import import_db, drop_db
from gms.net.serializers.meeting import MeetingSerializer


def setup_function():
    """Setup tests environment."""
    drop_db()
    import_db("tests/meeting/fixtures/general.json")
    import_db("tests/meeting/fixtures/basic_meeting.json")
    import_db("tests/meeting/fixtures/full_db.json")
    import_db("tests/meeting/fixtures/test.json")


def test_user_from_linked_objects(meeting):
    serializer = MeetingSerializer()
    data = serializer.serialize(meeting)

    # check user is present in full sync data
    assert "5bb5f311bff2ff000001fa62" in list(data["users"].keys())


def test_role_from_linked_objects(meeting):
    serializer = MeetingSerializer()
    data = serializer.serialize(meeting)

    # check role is present in full sync data
    assert "5bb5f311bff2ff000001fa5f" in list(data["roles"].keys())

