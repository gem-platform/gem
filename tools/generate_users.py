from mongoengine import connect
from names import get_full_name
from gem.db import Role, User

connect("gem",
        host="127.0.0.1", username="bhagavan",
        password="UZz5dGzZn@R*j\9%",
        authentication_source="admin",
        authentication_mechanism="SCRAM-SHA-1")

roles = Role.objects(name__in=["GBC", "Deputy", "Minister", "Guest"])

for role in roles:
    user = User(name=get_full_name(), roles=[role], password="123")
    user.save()
    print(user.name)
