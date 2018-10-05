from mongoengine import connect

from tools import drop_db

connect("mongoenginetest", host="mongomock://localhost")
drop_db()
