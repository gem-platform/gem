from flask import Blueprint, request, current_app, jsonify
from re import IGNORECASE
from bson.regex import Regex
from bson import ObjectId

api_autocomplete = Blueprint('api_autocomplete', __name__)


@api_autocomplete.route("/api/autocomplete", methods=["GET"])
def app_autocomplete():
    collection = request.args.get("collection", None)
    field = request.args.get("field", None)
    value = request.args.get("value", None)
    fields = request.args.getlist("fields[]") or []

    # no required arguments provided
    if not (collection and field and value):
        return jsonify({
            "success": False,
            "message": "Provide 'collection', 'field' and 'value' args"
        }), 400

    # find entities using regex
    regex = Regex(value)
    regex.flags ^= IGNORECASE
    db_collection = current_app.data.driver.db[collection]
    results = db_collection \
        .find({field: {"$regex": regex}}) \
        .limit(25)

    # map suggestions
    fields_to_get = fields + [field]
    suggestions = [
        {k: obj[k] for k in obj.keys() & fields_to_get}
        for obj in results
    ]

    # convert ObjectId to str
    for suggestion in suggestions:
        for key in suggestion:
            if isinstance(suggestion[key], ObjectId):
                suggestion[key] = str(suggestion[key])


    # return result
    return jsonify({"success": True, "suggestions": suggestions})


@api_autocomplete.route("/api/names", methods=["GET"])
def app_names():
    collection = request.args.get("collection", None)
    field = request.args.get("field", None)

    # no required arguments provided
    if not (collection and field):
        return jsonify({
            "success": False,
            "message": "Provide 'collection' and 'field' args"
        }), 400

    db_collection = current_app.data.driver.db[collection]
    results = db_collection.find({})

    # map suggestions
    suggestions = {str(obj["_id"]): obj[field] for obj in results}

    # return result
    return jsonify({"success": True, "items": suggestions})

