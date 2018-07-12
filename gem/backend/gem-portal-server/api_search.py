import os
from bson import ObjectId
from flask import Blueprint, jsonify, request, current_app
import sphinxapi


api_search = Blueprint('api_search', __name__)
db_host = os.environ.get('ES_HOST', "localhost")
c = sphinxapi.SphinxClient()
c.SetServer(db_host)


@api_search.route("/api/laws/search", methods=["GET"])
def laws_search():
    response = []
    query = request.args.get("query", "")
    search_result = c.Query(query)

    for match in search_result["matches"]:
        proposal_id = match["attrs"]["_id"]
        proposal = current_app.data.driver.db["laws"].find_one({"_id": ObjectId(proposal_id)})
        a = c.BuildExcerpts([proposal["content"]], 'mongo', query, {"limit": 1024})
        response.append({
            "_id": str(proposal["_id"]),
            "title": proposal["title"],
            "highlights": a[0]
        })

    return jsonify(response)
