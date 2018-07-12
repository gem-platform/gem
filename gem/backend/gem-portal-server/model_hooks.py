from bson import ObjectId
from flask import current_app
from gem.db.models import Zone


def user_replace_password(item, original):
    if not item.get("password", None):
        item["password"] = original.get("password", None)


def __get_parents_path(zone, result):
    db = current_app.data.driver.db
    parent_id = zone.get("parent", None)
    if parent_id:
        parent = db["zones"].find_one({"_id": parent_id})
        if parent:
            result.append(parent["name"])
            __get_parents_path(parent, result)
    return list(reversed(result))


def zone_update_path(item, original):
    zone = Zone.objects.get(id=ObjectId(item["_id"]))
    zone.save()  # call mongoengine hooks


def zone_update_path_items(items):
    for item in items:
        zone = Zone.objects.get(id=ObjectId(item["_id"]))
        zone.save()  # call mongoengine hooks

