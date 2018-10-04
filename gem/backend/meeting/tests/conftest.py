import pytest
from mongoengine import connect

from tools import drop_db

def pytest_addoption(parser):
    parser.addoption(
        "--dbhost", action="store", default="db", help="my option: type1 or type2"
    )

def pytest_report_header(config):
    db_host = config.getoption("dbhost")

    connect("gem_test_",
            host=db_host, username="bhagavan",
            password="UZz5dGzZn@R*j\9%",
            authentication_source="admin",
            authentication_mechanism="SCRAM-SHA-1")

    drop_db()
