import os
from pymongo import MongoClient


client = MongoClient(
    'db',
    username=os.environ['MONGO_USERNAME'],
    password=os.environ['MONGO_PASSWORD'],
    authSource=os.environ['MONGO_AUTH_SOURCE'],
    authMechanism=os.environ['MONGO_AUTH_MECHANISM']
)

laws = client.gem.laws

print("""
<sphinx:docset>
    <sphinx:schema>
    <sphinx:attr name="_id" type="string"/>
    <sphinx:attr name="type" type="string"/>
    <sphinx:field name="content"/>
    </sphinx:schema>
""")

id = 1
for law in laws.find({}):
    print("""
        <sphinx:document id='""" +str(id)+  """'>
        <_id>""" + str(law["_id"]) + """</_id>
        <type>laws</type>
        <content><![CDATA[[""" + law["content"] + """]]></content>
        </sphinx:document>
    """)
    id = id + 1

print("""</sphinx:docset>""")
