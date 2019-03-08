from random import choice
from mongoengine import connect
from names import get_full_name
from gem.db import Ballot, User

connect("gem",
        host="127.0.0.1", username="bhagavan",
        password="UZz5dGzZn@R*jj9%",
        authentication_source="admin",
        authentication_mechanism="SCRAM-SHA-1")

users = User.objects.all()
ballot = Ballot.objects.get(pk="5bb33dedf21a6902e6ea5c74")
ballot.finished = False

for user in users:
        value = choice(["yes", "no", "abstained"])
        ballot.set(user, value)

ballot.save()
