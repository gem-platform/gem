from inspect import getmembers, isclass

from flask import Blueprint, jsonify, request
import gem.db as db

API = Blueprint('api_debug', __name__)

ENTITY_MAP = {
    "workflowStages": db.WorkflowStage,
    "workflowTypes": db.WorkflowType,
    "proposals": db.Proposal,
    "meetings": db.Meeting,
    "roles": db.Role,
    "law": db.Law,
    "user": db.User,
    "ballot": db.Ballot,
    "comment": db.Comment,
    "meeting": db.Meeting,
    "official": db.Official,
    "zone": db.Zone
}


@API.route("/api/debug/reset", methods=["POST"])
def api_debug_reset():
    """Clean all the collections and fill DB with specified data."""
    # clean all the collections
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

    # get data
    data = request.get_json(force=True)
    for key in data:
        class_to_create = ENTITY_MAP.get(key, None)
        if not class_to_create:
            continue

        for entity in data[key]:
            entity = class_to_create(**entity)
            entity.save()

    # database has been reset
    return jsonify({"success": True, "message": "Done", "res": data})
