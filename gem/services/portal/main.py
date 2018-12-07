"""GEM Meeting Server Entry point"""
from eve import Eve
from flask_cors import CORS

from gem.utils.db import connect_db
from gem.utils.api import load_api

import model_hooks as mh

app = Eve()
CORS(app)

connect_db()
load_api(app)

# register model hooks
app.on_replace_users += mh.user_replace_password
app.on_replaced_zones += mh.zone_update_path
app.on_inserted_zones += mh.zone_update_path_items
