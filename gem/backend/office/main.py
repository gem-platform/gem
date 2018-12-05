from flask import Flask

from gem.utils.db import connect_db

from api_proposal import API_PROPOSAL
from api_zonal import API_ZONAL
from api_health import API_HEALTH

# connect to db
connect_db()

# register blueprints
APP = Flask("office")
APP.register_blueprint(API_HEALTH)
APP.register_blueprint(API_PROPOSAL)
APP.register_blueprint(API_ZONAL)

# run app
if __name__ == "__main__":
    APP.run(port=5001, host="0.0.0.0")
