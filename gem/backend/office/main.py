from flask import Flask

from gem.utils.db import connect_db
from gem.utils.api import load_api

# create app
app = Flask("office")

# configure app
connect_db()
load_api(app)
