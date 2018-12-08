from tools import import_db, drop_db
from gem.db import User, Role


def setup_function():
    """Setup tests environment."""
    drop_db()
    import_db("tests/meeting/fixtures/general.json")


def test_smoke():
    """Smoke test."""
    assert Role.objects.first().name == "Superuser"
    assert User.objects.first().name == "root"
    assert User.objects.first().main_role == Role.objects.first()
