# from gem.db import GemDatabase, Ballot, User

# db = GemDatabase("127.0.0.1", 27017, "gem_db_test")


# def setup_function():
#     user = User()
#     user.id = "user01"
#     user.name = "user"

#     ballot = Ballot()
#     ballot.secret = True
#     ballot.set(user, "yes")
#     db.ballots.save(ballot)


# def teardown_function():
#     db.drop()


# def test_ballot_save():
#     ballot = db.ballots.find_one({})
#     assert ballot is not None
#     assert ballot.secret is True
