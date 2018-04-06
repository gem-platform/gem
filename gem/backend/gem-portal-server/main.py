"""GEM Meeting Server Entry point"""
from eve import Eve
from flask import request, jsonify
from flask_cors import CORS
from mongoengine import connect
import sys
sys.path.append("../gem-server-common")
sys.path.append("./gem/gem-server-common")

from gem.db import User
connect("test1")

app = Eve()
CORS(app)


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    name = data.get("name")
    password = data.get("password")
    users = User.objects(name=name, password=password)
    print(users, name, password)
    if len(users) == 1:
        return jsonify({"success": True, "token": str(users[0].id)})
    return jsonify({"success": False})


if __name__ == '__main__':
    app.run()
