from inspect import getmembers, isclass
from json import loads

import gem.db as db


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

        print("DROP", c)
        c.drop_collection()

def without_keys(d, keys):
    return {k: v for k, v in d.items() if k not in keys}

def import_db(path):
    objs = {k:v for k, v in getmembers(db, isclass)}
    json = loads(open(path).read())

    for obj in json:
        obj_type = obj["$type"]
        obj_class = objs[obj_type]

        instance = obj_class(**without_keys(obj, ["$type"]))
        instance.save()
        print(instance)
