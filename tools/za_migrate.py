# Usage:
# python3 ./za_migrate.py | split -l 1
# xaa -> zones table
# xab -> persons table

import csv
import json
from bson import ObjectId

# Output -------------------------------------------------------------

zones = []
officials = []

# maps 

officials_new_id = {}

# Migrate officials ---------------------------------------------------

with open('data/Officials Names.csv', newline='') as file:
    reader = csv.reader(file, delimiter=',', quotechar='"')
    for row in reader:
        new_id = ObjectId()
        person_id = row[0]

        officials_new_id[person_id] = new_id

        person = {
            "_id": new_id,
            "name": row[2],
            "formOfAddress": row[1]
        }

        if row[3]:
            person["appendage"] = row[3]

        if row[4]:
            person["email"] = row[4]

        if row[5]:
            person["secretary"] = row[5] == "TRUE"
        
        if row[6]:
            person["gbc"] = row[6] == "TRUE"

        officials.append(person)

# Migrate zones ------------------------------------------------------

zone_levels = [
    {"file": "data/dbo_T_Continents.csv", "parent_row": -999, "name_row": 2},
    {"file": "data/GBC Zones.csv", "parent_row": 1, "name_row": 2},
    {"file": "data/Zonal Subregions.csv", "parent_row": 2, "name_row": 3},
    {"file": "data/States Subdivisions.csv", "parent_row": 3, "name_row": 2}
]

id_map = {}


for idx, level in enumerate(zone_levels):
    with open(level["file"], newline='') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        for row in reader:
            # get indexes
            id_index = 0
            cur_level = idx
            parent_index = level["parent_row"]
            name_index = level["name_row"]

            # generate new id for entity
            new_id = ObjectId()
            map_id = "{}_{}".format(cur_level, row[id_index])
            id_map[map_id] = new_id

            # create new entity
            entity = {
                "_id": new_id,
                "name": row[name_index]
            }

            # link with parent
            if idx > 0:
                prev_level = cur_level - 1
                parent_id = row[parent_index]
                map_parent_id = "{}_{}".format(prev_level, parent_id)
                entity["parent"] = id_map[map_parent_id]

            # GBC Zones.csv
            if idx == 1:
                persons = filter(lambda x: x != str(94), row[3:9])
                persons = list(map(lambda old_id: officials_new_id[old_id], persons))
                if persons:
                    entity["officials"] = persons.copy()

            # append
            zones.append(entity)


print(zones)
print(officials)