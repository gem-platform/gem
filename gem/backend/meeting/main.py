"""GEM Meeting Server Entry point"""
import os
import json
import logging
import logging.config

from gem.utils.db import connect_db

from gms.app import MeetingServerApplication
from gms.net import SocketIoEndpoint, HealthEndpoint

# configure loggers
with open("logging.json", "r", encoding="utf-8") as fd:
    logging.config.dictConfig(json.load(fd))

# we are starting
logging.getLogger("root").info("GEM Meeting Server is starting")

connect_db()

# configure application endpoints
MEETING_ENDPOINT = SocketIoEndpoint("0.0.0.0", 8090)
HEALTH_ENDPOINT = HealthEndpoint("0.0.0.0", 8099)

# run app
APP = MeetingServerApplication()
APP.endpoints.add(HEALTH_ENDPOINT)
APP.endpoints.add(MEETING_ENDPOINT)
APP.run()