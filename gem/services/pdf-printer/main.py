"""PDF printing service."""
from logging.config import fileConfig
from flask import Flask

from gem.utils.api import load_api

fileConfig("logging.conf")
APP = Flask("pdf")
load_api(APP)
