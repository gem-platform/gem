"""GEM Meeting Server Entry point"""
import os
from eve import Eve
from flask_cors import CORS
from mongoengine import connect

from api_search import api_search
from api_login import api_login
from api_autocomplete import api_autocomplete

db_host = os.environ.get('DB_HOST', "localhost")
db_username = os.environ.get('MONGO_USERNAME')
db_password = os.environ.get('MONGO_PASSWORD')
db_auth_source = os.environ.get('MONGO_AUTH_SOURCE')
db_auth_mechanism = os.environ.get('MONGO_AUTH_MECHANISM')
connect("gem", 
        host=db_host, username=db_username, password=db_password,
        authentication_source=db_auth_source,
        authentication_mechanism=db_auth_mechanism)


app = Eve()
app.register_blueprint(api_search)
app.register_blueprint(api_login)
app.register_blueprint(api_autocomplete)
CORS(app)


def event(response):
    for item in response.get("_items", []):
        if "password" in item:
            del item["password"]


def event2(item, original):
    if not item.get("password", None):
        item["password"] = original.get("password", None)


app.on_fetched_resource_users += event
app.on_replace_users += event2


if __name__ == '__main__':
    app.run(host='0.0.0.0')
