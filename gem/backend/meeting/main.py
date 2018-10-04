"""GEM Meeting Server Entry point"""
import os
import json
import logging
import logging.config

from mongoengine import connect

from gms.app import MeetingServerApplication
from gms.net import SocketIoEndpoint, HealthEndpoint

# configure loggers
with open("logging.json", "r", encoding="utf-8") as fd:
    logging.config.dictConfig(json.load(fd))

# we are starting
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
MEETING_ENDPOINT = SocketIoEndpoint("0.0.0.0", 8090)
HEALTH_ENDPOINT = HealthEndpoint("0.0.0.0", 8099)

# run app
APP = MeetingServerApplication()
APP.endpoints.add(HEALTH_ENDPOINT)
APP.endpoints.add(MEETING_ENDPOINT)
APP.run()
