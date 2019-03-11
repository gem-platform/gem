"""GEM Meeting Server Entry point"""
import os
import json
import logging
import logging.config
import ptvsd

from gem.utils.db import connect_db

from gms.app import MeetingServerApplication

# configure loggers
with open("logging.json", "r", encoding="utf-8") as fd:
    logging.config.dictConfig(json.load(fd))

# enable debugging
DEBUG = os.environ.get("DEBUG", None) in [1, "true"]
if DEBUG:
    logging.getLogger("root").critical("Debugging is enabled")
    ptvsd.enable_attach(("0.0.0.0", 9876))

# we are starting
logging.getLogger("root").info("GEM Meeting Server is starting")

connect_db()

# run app
APP = MeetingServerApplication()
APP.run()
