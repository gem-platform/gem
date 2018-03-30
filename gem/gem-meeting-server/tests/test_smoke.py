from gem.db import GemDatabase


def test_smoke():
    db = GemDatabase("127.0.0.1", 27017, "test_gem")
    assert len(db.proposals.all()) == 0
