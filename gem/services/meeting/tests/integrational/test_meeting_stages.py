from pytest import mark


def test_switch_stage_to_next(db, session):
    session.handshake(token=db.secretary.id, meeting=db.meeting.id)
    result = session.switch_stage(index=1)

    assert result.success is True
    assert session.meeting.stages.index == 1


def test_switch_stage_out_of_bounds(db, session):
    session.handshake(token=db.secretary.id, meeting=db.meeting.id)
    result = session.switch_stage(index=9999)

    assert result.success is False
    assert result.message == 'Unknown error: Stage index out of bounds'


def test_switch_stage_negative(db, session):
    session.handshake(token=db.secretary.id, meeting=db.meeting.id)
    result = session.switch_stage(index=-99)

    assert result.success is False
    assert result.message == 'Unknown error: Index can not be negative'


def test_reading_progress(db, session):
    session.handshake(token=db.secretary.id, meeting=db.meeting.id)
    session.switch_stage(index=1)
    result = session.reading_progress(quantity=.5)

    assert result.success is True
    assert session.meeting.stages.current.progress["count"] == 1
    assert session.meeting.stages.current.progress["values"] == {
        str(db.secretary.id): .5
    }


def test_vote(db, session):
    session.handshake(token=db.secretary.id, meeting=db.meeting.id)
    session.switch_stage(index=4)
    result = session.vote(value=True)

    votes = session.meeting.stages.current.ballot.votes

    assert result.success is True
    assert result.message == 'Accepted'
    assert len(votes) == 1
    assert db.secretary in map(lambda x: x.user, votes)


@mark.parametrize("value, expected", [
    (True, True),
    (False, False),
    (None, None),
])
def test_ballot_secret(db, session, value, expected):
    session.handshake(token=db.secretary.id, meeting=db.meeting.id)
    session.switch_stage(index=4)
    result = session.ballot_secret(value=value)

    assert result.success is True
    assert session.meeting.stages.current.ballot.secret is expected


@mark.parametrize("value, expected", [
    (0, 0),
    (1, 1),
    (.5, .5),
])
def test_ballot_threshold(db, session, value, expected):
    session.handshake(token=db.secretary.id, meeting=db.meeting.id)
    session.switch_stage(index=4)
    result = session.ballot_threshold(value=value)

    assert result.success is True
    assert session.meeting.stages.current.ballot.threshold == expected


@mark.parametrize("message, mark, quote, expected", [
    ("hello", "+", None, True),
    # ("", "+", None, False) validate empty comment
    # validate invalid marks
])
def test_comment(db, session, message, mark, quote, expected):
    session.handshake(token=db.secretary.id, meeting=db.meeting.id)
    session.switch_stage(index=2)
    
    result = session.comment(message=message, mark=mark, quote=quote)
    comments = session.meeting.stages.current.comments

    assert result.success is expected
    assert len(comments) == 1
    assert comments[0].content == message
    assert comments[0].mark == mark

    if comments[0].quote:
        assert comments[0].quote.text == quote


def test_request_floor(db, session):
    session.handshake(token=db.secretary.id, meeting=db.meeting.id)
    session.switch_stage(index=3)
    result = session.request_floor()

    assert result.success is True
    assert db.secretary in session.meeting.stages.current.queue


def test_withdraw_from_queue(db, session):
    session.handshake(token=db.secretary.id, meeting=db.meeting.id)
    session.switch_stage(index=3)
    session.request_floor()
    result = session.withdraw_from_queue()

    assert result.success is True
    assert not session.meeting.stages.current.queue  # queue is empty


def test_remove_from_queue(db, session):
    session.handshake(token=db.secretary.id, meeting=db.meeting.id)
    session.switch_stage(index=3)
    session.request_floor()
    result = session.remove_from_queue(id=db.secretary.id)

    assert result.success is True
    assert not session.meeting.stages.current.queue  # queue is empty


def test_give_voice(db, session):
    session.handshake(token=db.secretary.id, meeting=db.meeting.id)
    session.switch_stage(index=3)
    session.request_floor()
    result = session.give_voice(to=db.secretary.id)

    assert result.success is True
    assert session.meeting.stages.current.speaker == db.secretary  # queue is empty

