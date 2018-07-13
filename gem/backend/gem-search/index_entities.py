import os
from pymongo import MongoClient


client = MongoClient(
    'gem-database',
    username=os.environ['MONGO_USERNAME'],
    password=os.environ['MONGO_PASSWORD'],
    authSource=os.environ['MONGO_AUTH_SOURCE'],
    authMechanism=os.environ['MONGO_AUTH_MECHANISM']
)

collections = {
    "users": {"field": "name"},
    "officials": {"field": "name"},
    "zones": {"field": "name"},
    "proposals": {"field": "title"},
    "meetings": {"field": "title"},
    "roles": {"field": "name"},
    "comments": {"field": "content"}
    # "laws": {"field": "title"},
}

print("""
<sphinx:docset>
    <sphinx:schema>
    <sphinx:attr name="_id" type="string"/>
    <sphinx:attr name="type" type="string"/>
    <sphinx:field name="name"/>
    </sphinx:schema>
""")

id = 10000
for collection, options in collections.items():
    db_collection = client.gem[collection]
    field = options["field"]

    for model in db_collection.find({}):
        print("""
            <sphinx:document id='""" + str(id) + """'>
            <_id>""" + str(model["_id"]) + """</_id>
            <type>""" + collection + """</type>
            <name><![CDATA[[""" + model[field] + """]]></name>
            </sphinx:document>
        """)
        id = id + 1
    id += 10000


print("""</sphinx:docset>""")
