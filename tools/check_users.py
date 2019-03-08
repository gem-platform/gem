import csv

from mongoengine import connect
from gem.db import Role, User

connect("gem",
        host="gemapp.in", username="bhagavan",
        password="UZz5dGzZn@R*jj9%",
        authentication_source="admin",
        authentication_mechanism="SCRAM-SHA-1")


with open('passwords.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        obj = User.objects(name=row[0]).first()
        if not obj:
            print(row[0] + " doesn't exist")
            obj = User(name=row[0], password=row[1])
        if obj and (obj.password != row[1]):
            print(row[0] + " exist but password is different")
            obj.password = row[1]
        obj.save()
        # print(obj, row[0], row[1])


#for user in User.objects.all():
#    print(user.name)
