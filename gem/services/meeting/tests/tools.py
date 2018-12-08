from inspect import getmembers, isclass
from json import loads

import gem.db as db

class Db:
    def __init__(self):
        self.data = {}

    def set(self, id, value):
        self.data[id] = value

    def __getattr__(self, attr):
        return self.data[attr]

def drop_db():
    """Drops all the entities from Database."""
    # clean all the collections
    for (_, c) in getmembers(db, isclass):
        if c is db.GemDocument:
            continue

        if not issubclass(c, db.GemDocument):
            continue

        if not hasattr(c, "drop_collection"):
            continue

        c.drop_collection()

def without_keys(d, keys):
    return {k: v for k, v in d.items() if k not in keys}

def import_db(path):
    result = Db()

    objs = {k:v for k, v in getmembers(db, isclass)}
    json = loads(open(path).read())

    for obj in json:
        data = without_keys(obj, ["$type", "$alias"])

        obj_type = obj["$type"]
        obj_class = objs[obj_type]

        # check if object already exist
        exist = obj_class.objects(pk=obj["id"]).first()
        if exist:
            exist.delete()

        instance = obj_class(**data)
        instance.save()

        if "$alias" in obj:
            result.set(obj["$alias"], instance)

    return result
