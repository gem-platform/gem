from gem.db import GemDatabase, User

db = GemDatabase("127.0.0.1", 27017, "gem_db_test")


def setup_function():
    user = User(name="secretary das")
    db.users.save(user)


def teardown_function():
    db.drop()


def test_user_save():
    user = db.users.find_one({"name": "secretary das"})
    assert user is not None
    assert user.name == "secretary das"


def test_find_by_name():
    db.users.save(User(name="user 01"))
    db.users.save(User(name="user 02"))
    db.users.save(User(name="user 03"))

    users = db.users.find_by_name("user 02")
    assert len(users) == 1
    assert users[0].name == "user 02"
