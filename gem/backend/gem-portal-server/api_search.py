import os

from flask import Blueprint, jsonify, request, current_app
from elasticsearch import Elasticsearch
from misc import remove_html_tags

api_search = Blueprint('api_search', __name__)
db_host = os.environ.get('ES_HOST', "localhost")
es = Elasticsearch([db_host])


@api_search.route("/api/laws/search", methods=["GET"])
def laws_search():
    query = request.args.get("query", "")
    result = es.search(index="gem", body={
        "query": {
            "multi_match": {
                "query": query,
                "fuzziness": "AUTO",
                "fields": ["title", "content"]
            }
        },
        "highlight": {
            "fields": {
                "content": {},
                "title": {}
            }
        }
    })
    return jsonify(result)


@api_search.route("/api/laws/rebuild_index", methods=["GET"])
def update_laws_index():
    es.indices.delete(index='gem')
    laws = current_app.data.driver.db["laws"].find({})
    for law in list(laws):
        law_id = str(law["_id"])
        es.index(index="gem", doc_type="law", id=law_id, body={
            "title": law["title"],
            "content": remove_html_tags(law["content"])
        })

    return jsonify({"success": True})


# def on_inserted_laws(items):
#     db_host = os.environ.get('ES_HOST', "localhost")
#     es = Elasticsearch([db_host])

#     for item in items:
#         item2 = item.copy()
#         item2["content"] = remove_html_tags(item2["content"])
#         item2["mongo_id"] = str(item2["_id"])
#         del item2["_id"]
#         es.index(index="gem", doc_type="law", id=item["index"], body=item2)

# app.on_inserted_laws += on_inserted_laws