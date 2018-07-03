from flask import Blueprint, request, current_app
from re import IGNORECASE
from bson.json_util import dumps
from bson.regex import Regex

api_autocomplete = Blueprint('api_autocomplete', __name__)


@api_autocomplete.route("/api/autocomplete", methods=["GET"])
def app_autocomplete():
    collection = request.args.get("collection", None)
    field = request.args.get("field", None)
    value = request.args.get("value", None)
    fields = request.args.getlist("fields[]", [])

    # no required arguments provided
    if not (collection and field and value):
        return dumps({
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

    # return result
    return dumps({"success": True, "suggestions": suggestions})
