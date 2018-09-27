from flask import Blueprint, jsonify, request
from mongoengine import DoesNotExist
from gem.db import User

api_login = Blueprint('api_login', __name__)


@api_login.route("/api/auth/login", methods=["POST"])
def api_auth_login():
    data = request.get_json(force=True)
    login = data.get("login")
    password = data.get("password")

    # no login or password provided
    if not (login and password):
        return jsonify({
            "success": False,
            "message": "Login and password required"
        }), 401

    # try to fetch user with specified credentials
    try:
        user = User.objects.get(name=login, password=password)
        return jsonify({"success": True, "token": str(user.id)})
    except DoesNotExist:
        return jsonify({
            "success": False, "message": "Login failed"
        }), 401


@api_login.route("/api/auth/logout", methods=["POST"])
def api_auth_logout():
    return jsonify({"success": True})


@api_login.route("/api/auth/user", methods=["GET"])
def api_auth_user():
    cookie = request.cookies.get('auth._token.local', None)
    if not cookie:
        return jsonify({"message": "no cookie provided"}), 401

    token = cookie[len("Bearer%20"):]
    if token == "undefined":
        return jsonify({"message": "no token provided"}), 401

    try:
        user = User.objects.get(id=token)
        return jsonify({
            "user": {
                "id": str(user.id),
                "name": user.name,
                "token": str(user.id),
                "scopes": user.permissions
            }
        })
    except DoesNotExist:
        return jsonify({"message": "user not found " + token}), 401
