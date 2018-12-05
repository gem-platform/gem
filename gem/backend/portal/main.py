"""GEM Meeting Server Entry point"""
from os import environ
from eve import Eve
from flask_cors import CORS

from gem.utils.db import connect_db

from api_search import api_search
from api_login import api_login
from api_autocomplete import api_autocomplete
from api_debug import API_DEBUG
from api_health import api_health

import model_hooks as mh

debug = environ.get("DEBUG", "false") == "true"

connect_db()

app = Eve()
app.register_blueprint(api_search)
app.register_blueprint(api_login)
app.register_blueprint(api_autocomplete)
app.register_blueprint(api_health)
if debug:
    app.register_blueprint(API_DEBUG)
CORS(app)

# register model hooks
app.on_replace_users += mh.user_replace_password
app.on_replaced_zones += mh.zone_update_path
app.on_inserted_zones += mh.zone_update_path_items

# run as standard script, not by gunicorn
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
