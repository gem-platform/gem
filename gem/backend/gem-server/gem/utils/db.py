from os import environ
from mongoengine import connect


def connect_db():
    db_host = environ.get("DB_HOST", "localhost")
    db_username = environ.get("MONGO_USERNAME")
    db_password = environ.get("MONGO_PASSWORD")
    db_auth_source = environ.get("MONGO_AUTH_SOURCE")
    db_auth_mechanism = environ.get("MONGO_AUTH_MECHANISM")
    connect("gem",
            host=db_host, username=db_username, password=db_password,
            authentication_source=db_auth_source,
            authentication_mechanism=db_auth_mechanism)
