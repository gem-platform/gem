from gem.db import GemDatabase, Role

db = GemDatabase("127.0.0.1", 27017, "gem_db_test")


def setup_function():
    role = Role(name="GBC")
    db.roles.save(role)


def teardown_function():
    db.drop()


def test_role_save():
    role = db.roles.find_one({"name": "GBC"})
    assert role is not None
    assert role.name == "GBC"


def test_find_by_name():
    db.roles.save(Role(name="user 01"))
    db.roles.save(Role(name="user 02"))
    db.roles.save(Role(name="user 03"))

    role = db.roles.find_by_name("user 02")
    assert role is not None
    assert role.name == "user 02"
