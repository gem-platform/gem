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

PROPOSALS = {
    "schema": {
        "title": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "index": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "stage": {
            "type": "string"
        },
        "content": {
            "type": "string",
            "required": True,
            "empty": False
        }
    }
}

LAWS = {
    "schema": {
        "title": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "index": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "content": {
            "type": "string",
            "required": True,
            "empty": False
        }
    }
}

USERS = {
    "schema": {
        "name": {
            "type": "string",
            "required": True,
            "empty": False
        },
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

ROLES = {
    "schema": {
        "name": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "permissions": {"type": "list"}
    }
}

MEETINGS = {
    "schema": {
        "title": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "agenda": {"type": "string"},
        "start": {
            "type": "datetime",
            "required": True,
            "empty": False
        },
        "end": {
            "type": "datetime",
            "required": True,
            "empty": False
        },
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

OFFICIALS = {
    "schema": {
        "name": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "formOfAddress": {
            "type": "string",
            "required": True,
            "empty": False,
            "allowed": ["P", "M", "B", "S", "G", "N"]
        },
        "email": {
            "type": "string"
        },
        "appendage": {
            "type": "string"
        },
        "secretary": {
            "type": "bool"
        },
        "gbc": {
            "type": "bool"
        }
    }
}

ZONES = {
    "schema": {
        "name": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "parent": {
            "type": "objectid",
            "data_relation": {
                "resource": "zones"
            }
        },
        "officials": {
            "type": "list",
            "schema": {
                "type": "objectid",
                "data_relation": {
                    "resource": "zones"
                }
            }
        },
    }
}

DOMAIN = {
    "proposals": PROPOSALS,
    "users": USERS,
    "roles": ROLES,
    "meetings": MEETINGS,
    "laws": LAWS,
    "officials": OFFICIALS,
    "zones": ZONES
}
