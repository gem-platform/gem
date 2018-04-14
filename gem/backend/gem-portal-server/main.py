"""GEM Meeting Server Entry point"""
import os
from eve import Eve
from flask import request, jsonify
from flask_cors import CORS
from eve.auth import TokenAuth
from mongoengine import connect
import sys
sys.path.append("../gem-server-common")
sys.path.append("./gem/gem-server-common")

from gem.db import User

db_host = os.environ.get('DB_HOST', "localhost")
connect("test", host=db_host)


class MyTokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        # use Eve's own db driver; no additional connections/resources are used
        print(token)
        return True


app = Eve()  # auth=MyTokenAuth)
CORS(app)


@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    name = data.get("name")
    password = data.get("password")
    users = User.objects(name=name, password=password)
    print(users, name, password)
    if len(users) == 1:
        return jsonify({"success": True, "token": str(users[0].id)})
    return jsonify({"success": False}), 401


@app.route("/api/auth/user", methods=["GET"])
def user():
    cookie = request.cookies.get('auth._token.local', None)
    if not cookie:
        return jsonify({}), 401

    token = cookie[len("Bearer%20"):]
    if token == "undefined":
        return jsonify({}), 401

    print(token)
    users = User.objects(id=token)
    if len(users) == 1:
        return jsonify({
            "user": {
                "name": users[0].name,
                "token": str(users[0].id)
            }
        })
    else:
        return jsonify({}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0')
