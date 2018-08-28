from pytest import fixture
from mongoengine import connect

from tools import drop_db

connect("gem_test_",
        host="gem-database", username="bhagavan",
        password="UZz5dGzZn@R*j\9%",
        authentication_source="admin",
        authentication_mechanism="SCRAM-SHA-1")

drop_db()
