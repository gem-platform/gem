from importlib import import_module
from flask import Flask

from gem.utils.db import connect_db

# connect to db
connect_db()

# register blueprints
API_MODULES = ["api.health", "api.proposal", "api.zonal"]
APPLICATION = Flask("office")

# load all the API modules
for module_name in API_MODULES:
    module = import_module(module_name)
    var = getattr(module, "API")
    APPLICATION.register_blueprint(var)

# run app
if __name__ == "__main__":
    APPLICATION.run(port=5001, host="0.0.0.0")
