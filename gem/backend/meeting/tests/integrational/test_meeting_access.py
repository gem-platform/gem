from tools import import_db, drop_db


def test_access_meeting_with_superusers_privileges(db, session):
    """User with '*' permissions should be able to join meeting."""
    response = session.handshake(token=db.superuser.id, meeting=db.meeting.id)
    assert response.success is True


def test_access_with_join_permissions(db, session):
    """User listed in permissions should be able to access meeting."""
    response = session.handshake(token=db.gbc_user.id, meeting=db.meeting.id)
    assert response.success is True


def test_access_with_join_role_permissions(db, session):
    """User listed role in permissions should be able to access meeting."""
    response = session.handshake(token=db.deputy_user.id, meeting=db.meeting.id)
    assert response.success is True


def test_access_with_no_join_permissions(db, session):
    """User listed role in permissions should be able to access meeting."""
    response = session.handshake(token=db.guest.id, meeting=db.meeting.id)
    assert response.success is False


def test_access_request(db, meetings, session, session2):
    """User listed role in permissions should be able to access meeting."""
    meeting_id = str(db.meeting.id)

    session.handshake(token=db.superuser.id, meeting=db.meeting.id)
    assert db.guest not in meetings.active[meeting_id].allowed_users

    session2.handshake(token=db.guest.id, meeting=db.meeting.id)
    session2.request_access(token=db.guest.id)
    session.grant_access(token=db.guest.id, value=True)

    assert db.guest in meetings.active[meeting_id].allowed_users


def test_access_wrong_meeting(db, session):
    """User listed role in permissions should be able to access meeting."""
    response = session.handshake(token=db.superuser.id, meeting="5a5deebeb53856badbadffff")
    assert response.success is False


def test_access_wrong_meeting_id(db, session):
    """User listed role in permissions should be able to access meeting."""
    response = session.handshake(token=db.superuser.id, meeting="ololo alala")
    assert response.success is False


def test_empty_meeting_shoud_close(db, session, meetings):
    """Meeting should be closed if there is no personos any more."""
    session.handshake(token=db.superuser.id, meeting=db.meeting.id)
    session.handshake(token=db.superuser.id, meeting=db.meeting2.id)

    ids = list(map(str, meetings.active.keys()))

    assert len(meetings.active.keys()) == 1
    assert ids[0] == str(db.meeting2.id)


def test_meeting_with_users_should_close(db, session, session2, meetings):
    """Meeting should be closed if there is no personos any more."""
    session.handshake(token=db.superuser.id, meeting=db.meeting.id)
    session2.handshake(token=db.superuser.id, meeting=db.meeting.id)
    session2.handshake(token=db.superuser.id, meeting=db.meeting2.id)

    ids = list(meetings.active.keys())

    assert len(meetings.active.keys()) == 2
    assert str(db.meeting.id) in ids
    assert str(db.meeting2.id) in ids
