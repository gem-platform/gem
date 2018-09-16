"""GEM Meeting Server Entry point"""
import os
import logging
import logging.config

from mongoengine import connect

from gms.app import MeetingServerApplication
from gms.net import SocketIoEndpoint

# setup logging
logging.config.fileConfig("logging.conf")
logging.getLogger("root").info("GEM Meeting Server is starting")

# connect to DB
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USERNAME = os.environ.get("MONGO_USERNAME")
DB_PASSWORD = os.environ.get("MONGO_PASSWORD")
DB_AUTH_SOURCE = os.environ.get("MONGO_AUTH_SOURCE")
DB_AUTH_MECHANISM = os.environ.get("MONGO_AUTH_MECHANISM")
connect("gem",
        host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD,
        authentication_source=DB_AUTH_SOURCE,
        authentication_mechanism=DB_AUTH_MECHANISM)

# configure application endpoints
ENDPOINT = SocketIoEndpoint("0.0.0.0", 8090)

# run app
APP = MeetingServerApplication()
APP.endpoints.add(ENDPOINT)
APP.run()
