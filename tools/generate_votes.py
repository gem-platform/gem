from random import choice
from mongoengine import connect
from names import get_full_name
from gem.db import Ballot, User

connect("gem",
        host="127.0.0.1", username="bhagavan",
        password="UZz5dGzZn@R*j\9%",
        authentication_source="admin",
        authentication_mechanism="SCRAM-SHA-1")

users = User.objects.all()
ballot = Ballot.objects.get(pk="5bb212c13957cb08ddce667d")
ballot.finished = False

for user in users:
        value = choice(["yes", "no", "abstained"])
        ballot.set(user, value)

ballot.secret = True
ballot.save()