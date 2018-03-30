from gem.db import GemDatabase, Proposal

db = GemDatabase("127.0.0.1", 27017, "gem_db_test")


def setup_function():
    proposal = Proposal()
    proposal.title = "title"
    proposal.index = "001.002.003"
    proposal.content = "some content"
    db.proposals.save(proposal)


def teardown_function():
    db.drop()


def test_proposal_save():
    proposal = db.proposals.find_one({"title": "title"})
    assert proposal is not None
    assert proposal.title == "title"
    assert proposal.index == "001.002.003"
    assert proposal.content == "some content"


def test_find_by_title():
    db.proposals.save(Proposal(index="01", title="test 01"))
    db.proposals.save(Proposal(index="02", title="test 02"))
    db.proposals.save(Proposal(index="03", title="test 03"))

    proposals = db.proposals.find_by_title("title")
    assert len(proposals) == 1
    assert proposals[0].title == "title"


def test_find_by_index():
    proposal = db.proposals.find_by_index("001.002.003")
    assert proposal is not None
    assert proposal.index == "001.002.003"
