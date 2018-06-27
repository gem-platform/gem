import os
db_host = os.environ.get('DB_HOST', "localhost")

URL_PREFIX = "api"
MONGO_URI = "mongodb://"+db_host+":27017/gem"
DEBUG = True
IF_MATCH = False
CACHE_EXPIRES = 1
PAGINATION = False

MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_AUTH_SOURCE = os.environ.get('MONGO_AUTH_SOURCE')
MONGO_AUTH_MECHANISM = os.environ.get('MONGO_AUTH_MECHANISM')

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

proposal = {
    "schema": {
        "title": {
            "type": "string"
        },
        "index": {
            "type": "string"
        },
        "stage": {
            "type": "string"
        },
        "content": {
            "type": "string"
        }
    }
}

laws = {
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

users = {
    "schema": {
        "name": {"type": "string"},
        "roles": {
            "type": "list",
            "schema": {
                "type": "objectid",
                "data_relation": {
                    "resource": "roles"
                }
            }
        },
        "password": {"type": "string"}
    }
}

roles = {
    "schema": {
        "name": {"type": "string"},
        "permissions": {"type": "list"}
    }
}

meetings = {
    "schema": {
        "title": {"type": "string"},
        "agenda": {"type": "string"},
        "start": {"type": "datetime"},
        "end": {"type": "datetime"},
        "proposals": {
            "type": "list",
            "schema": {
                "type": "objectid",
                "data_relation": {
                    "resource": "proposals"
                }
            }
        },
        "permissions": {
            "type": "list",
            "schema": {
                "type": "dict",
                "schema": {
                    "scope": {"type": "string"},
                    "user": {"type": "objectid", "data_relation": {"resource": "users"}},
                    "role": {"type": "objectid", "data_relation": {"resource": "roles"}}
                }
            }
        }
    }
}


DOMAIN = {
    "proposals": proposal,
    "users": users,
    "roles": roles,
    "meetings": meetings,
    "laws": laws
}
