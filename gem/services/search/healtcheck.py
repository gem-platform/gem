"""Health Check server."""

from os import environ
from sphinxapi import SphinxClient


SEARCH_HOST = environ.get("ES_HOST", "localhost")
CLIENT = SphinxClient()
CLIENT.SetServer(SEARCH_HOST)


try:
    STATUS = CLIENT.Status()
    UPTIME = int(STATUS[0][1].decode("utf-8"))

    if UPTIME <= 0:
        raise Exception("Search is down")

    exit(0)
except Exception:
    exit(1)
