from tools import import_db, drop_db
from gem.db import Proposal, Comment

def setup_function():
    """Setup tests environment."""
    drop_db()
    import_db("tests/meeting/fixtures/general.json")
    import_db("tests/meeting/fixtures/basic_meeting.json")
    import_db("tests/meeting/fixtures/full_db.json")


def test_show_comments_for_appropriate_stage(meeting):
    acquaintance_stage = meeting.stages.switch_to(1)
    comment_stages = map(lambda x: x.stage.name, acquaintance_stage.comments)
    assert list(comment_stages) == ["Review"]

    acquaintance_stage = meeting.stages.switch_to(6)
    comment_stages = map(lambda x: x.stage.name, acquaintance_stage.comments)
    assert list(comment_stages) == ["Final Vote"]


def test_show_ballots_for_appropriate_stage(meeting):
    acquaintance_stage = meeting.stages.switch_to(1)
    assert acquaintance_stage.ballot.stage.name == "Review"

    acquaintance_stage = meeting.stages.switch_to(7)
    assert acquaintance_stage.ballot.stage.name == "Final Vote"


def test_ballot_and_ballot_results_shares_same_ballot_object(meeting):
    ballot = meeting.stages[3]  # ballot stage
    ballot_results = meeting.stages[4] # ballot results stage
    assert ballot.ballot == ballot_results.ballot
