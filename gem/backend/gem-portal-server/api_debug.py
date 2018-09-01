from inspect import getmembers, isclass

from flask import Blueprint, jsonify
import gem.db as db

api_debug = Blueprint('api_debug', __name__)


@api_debug.route("/api/debug/reset", methods=["POST"])
def api_debug_reset():
    for (_, c) in getmembers(db, isclass):
        if c is db.GemDocument:
            continue

        if not issubclass(c, db.GemDocument):
            continue

        if not hasattr(c, "drop_collection"):
            continue

        c.drop_collection()

    # create an essential entities
    role = db.Role(name="Superuser", permissions=["*"], priority=999)
    role.save()

    user = db.User(name="root", password="root", roles=[role])
    user.save()

    # database has been reset
    return jsonify({"success": True, "message": "Done"})


