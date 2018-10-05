from tools import import_db, drop_db


def setup_function():
    """Setup tests environment."""
    drop_db()
    import_db("tests/integrational/fixtures/general.json")


def test_access_meeting_with_superusers_privileges(meetings):
    """User with '*' permissions should be able to join meeting."""
    data = {"token": "5bb73d70206d3a000059bb85", "meeting": "5a5deebeb5385609a9c9face"}
    response = meetings.command("handshake", "session01", data)
    assert response["success"] is True


def test_access_with_join_permissions(meetings):
    """User listed in permissions should be able to access meeting."""
    data = {"token": "5bb73d70206d3a000059bb86", "meeting": "5a5deebeb5385609a9c9face"}
    response = meetings.command("handshake", "session01", data)
    assert response["success"] is True


def test_access_with_join_role_permissions(meetings):
    """User listed role in permissions should be able to access meeting."""
    data = {"token": "5bb73cac20847c0000da8293", "meeting": "5a5deebeb5385609a9c9face"}
    response = meetings.command("handshake", "session01", data)
    assert response["success"] is True


def test_access_with_no_join_permissions(meetings):
    """User listed role in permissions should be able to access meeting."""
    data = {"token": "5bb73cac20847c0000da8295", "meeting": "5a5deebeb5385609a9c9face"}
    response = meetings.command("handshake", "session01", data)
    assert response["success"] is False


# def test_access_wrong_meeting(meetings):
#     """User listed role in permissions should be able to access meeting."""
#     data = {"token": "5bb73cac20847c0000da8295", "meeting": "5a5deebeb5385609a9c9facf"}
#     response = meetings.command("handshake", "session01", data)
#     assert response["success"] is False
#     assert response["message"] == "Meeting not found"
