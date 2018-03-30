from gem.db import GemDatabase, Proposal

db = GemDatabase("127.0.0.1", 27017, "gem_db_test")


def setup_function():
    db.proposals.save(Proposal(index="01", title="test 01"))
    db.proposals.save(Proposal(index="02", title="test 02"))
    db.proposals.save(Proposal(index="03", title="test 03"))


def teardown_function():
    db.drop()


def test_count_all():
    assert db.proposals.count({}) == 3


def test_count_query():
    assert db.proposals.count({"title": "test 01"}) == 1


def test_map_model():
    proposal = db.proposals.find_one({"title": "test 01"})
    assert type(proposal) is Proposal
    assert proposal.id is not None
    assert proposal.title == "test 01"


def test_map_db():
    db.proposals.save(Proposal(title="test 99"))
    proposal = db.proposals.find_one({"title": "test 99"})
    assert proposal.title == "test 99"


def test_save():
    proposal = Proposal(index="01", title="Test")
    db.proposals.save(proposal)
    assert proposal.id is not None


def test_update():
    count = db.proposals.count({})

    proposal = db.proposals.find_one({"title": "test 01"})
    proposal.title = "test XYZ"
    db.proposals.save(proposal)

    proposal = db.proposals.find_one({"title": "test XYZ"})
    assert proposal.title == "test XYZ"
    assert db.proposals.count({}) == count
