import os
db_host = os.environ.get('DB_HOST', "localhost")

URL_PREFIX = "api"
MONGO_URI = "mongodb://"+db_host+":27017/test"
DEBUG = True

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

proposal = {
    "schema": {
        "title": {
            "type": "string"
        },
        "index": {
            "type": "string"
        },
        "content": {
            "type": "string"
        }
    }
}


DOMAIN = {
    "proposal": proposal
}
