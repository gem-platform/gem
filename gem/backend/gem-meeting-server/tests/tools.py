from inspect import getmembers, isclass
import gem.db as db


def drop_db():
    """Drops all the entities from Database."""
    # clean all the collections
    for (_, c) in getmembers(db, isclass):
        print(c, c is db.GemDocument, issubclass(c, db.GemDocument), hasattr(c, "drop_collection"))

        if c is db.GemDocument:
            continue

        if not issubclass(c, db.GemDocument):
            continue

        if not hasattr(c, "drop_collection"):
            continue

        c.drop_collection()
