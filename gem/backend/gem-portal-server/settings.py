import os
db_host = os.environ.get('DB_HOST', "localhost")

URL_PREFIX = "api"
MONGO_URI = "mongodb://"+db_host+":27017/gem"
DEBUG = True
IF_MATCH = False
CACHE_EXPIRES = 1

MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_AUTH_SOURCE = os.environ.get('MONGO_AUTH_SOURCE')
MONGO_AUTH_MECHANISM = os.environ.get('MONGO_AUTH_MECHANISM')

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

MONGO_QUERY_BLACKLIST = ['$where']


PROPOSALS = {
    "datasource": {
        "default_sort": [
            ("title", 1)
        ]
    },
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
        "workflow": {
            "type": "objectid",
            "data_relation": {
                "resource": "workflowTypes",
                "embeddable": True
            }
        },
        "stage": {
            "type": "objectid",
            "data_relation": {
                "resource": "workflowStages",
                "embeddable": True
            }
        },
        "content": {
            "type": "string",
            "required": True,
            "empty": False
        }
    }
}

LAWS = {
    "datasource": {
        "default_sort": [
            ("title", 1)
        ]
    },
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
    "datasource": {
        "projection": {
            "password": 0
        },
        "default_sort": [
            ("name", 1)
        ]
    },
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
                    "resource": "roles",
                    "embeddable": True
                }
            }
        },
        "password": {"type": "string"}
    }
}

ROLES = {
    "datasource": {
        "default_sort": [
            ("name", 1)
        ]
    },
    "schema": {
        "name": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "permissions": {
            "type": "list"
        },
        "priority": {
            "type": "integer",
            "required": True
        }
    }
}

MEETINGS = {
    "datasource": {
        "default_sort": [
            ("start", 1)
        ]
    },
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
                    "resource": "proposals",
                    "embeddable": True
                }
            }
        },
        "permissions": {
            "type": "list",
            "schema": {
                "type": "dict",
                "schema": {
                    "scope": {"type": "string"},
                    "user": {
                        "type": "objectid",
                        "data_relation": {"resource": "users"}
                    },
                    "role": {
                        "type": "objectid",
                        "data_relation": {"resource": "roles"}
                    }
                }
            }
        }
    }
}

OFFICIALS = {
    "datasource": {
        "default_sort": [
            ("name", 1)
        ]
    },
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
            "type": "boolean"
        },
        "gbc": {
            "type": "boolean"
        },
        "cachedZones": {
            "readonly": True,
            "type": "list",
            "schema": {
                "type": "objectid",
                "data_relation": {
                    "resource": "zones",
                    "embeddable": True
                }
            }
        }
    }
}

ZONES = {
    "datasource": {
        "default_sort": [
            ("name", 1)
        ]
    },
    "schema": {
        "name": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "parent": {
            "type": "objectid",
            "data_relation": {
                "resource": "zones",
                "embeddable": True
            }
        },
        "officials": {
            "type": "list",
            "schema": {
                "type": "objectid",
                "data_relation": {
                    "resource": "officials",
                    "embeddable": True
                }
            }
        },
        "path": {
            "type": "list",
            "schema": {
                "type": "string",
                "empty": False,
            }
        },
        "cachedOfficials": {
            "readonly": True,
            "type": "list",
            "schema": {
                "type": "objectid",
                "data_relation": {
                    "resource": "officials",
                    "embeddable": True
                }
            }
        }
    }
}

COMMENTS = {
    "schema": {
        "user": {
            "type": "objectid",
            "data_relation": {
                "resource": "users",
                "embeddable": True
            }
        },
        "proposal": {
            "type": "objectid",
            "data_relation": {
                "resource": "proposals",
                "embeddable": True
            }
        },
        "content": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "mark": {
            "type": "string",
            "required": True,
            "empty": False
        }
    }
}

WORKFLOW_STAGES = {
    "schema": {
        "name": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "description": {
            "type": "string"
        },
    }
}

WORKFLOW_TYPES = {
    "schema": {
        "name": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "stages": {
            "type": "list",
            "schema": {
                "type": "objectid",
                "data_relation": {
                    "resource": "workflowStages",
                    "embeddable": True
                }
            }
        }
    }
}

DOMAIN = {
    "proposals": PROPOSALS,
    "users": USERS,
    "roles": ROLES,
    "meetings": MEETINGS,
    "laws": LAWS,
    "officials": OFFICIALS,
    "zones": ZONES,
    "comments": COMMENTS,
    "workflowStages": WORKFLOW_STAGES,
    "workflowTypes": WORKFLOW_TYPES
}
