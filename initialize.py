import json
import os

import rjsmin
from girder_client import GirderClient

gc = GirderClient(apiUrl="https://girder.local.xarthisius.xyz/api/v1")
gc.authenticate(username="admin", password=os.environ["GIRDER_PASSWORD"])

# Delete all existing items
for form in gc.get("form"):
    gc.delete("form/%s" % form["_id"])

# Delete all existing depositions
for deposition in gc.get("deposition", parameters={"limit": 1000}):
    gc.delete("deposition/%s" % deposition["_id"])

for collection in gc.get("/collection", parameters={"text": "HTMAX"}):
    gc.delete("collection/%s" % collection["_id"])

group = gc.get("/group", parameters={"text": "Testers", "exact": True})
if not group:
    group = gc.post("/group", parameters={"name": "Testers"})
else:
    group = group[0]

user = gc.get("/user/me")

creator = {
    "givenName": user["firstName"],
    "familyName": user["lastName"],
    "name": f"{user['firstName']} {user['lastName']}",
}

access = {
    "groups": [
        {
            "description": "",
            "flags": [],
            "id": group["_id"],
            "level": 2,
            "name": group["name"],
        }
    ],
    "users": [
        {
            "flags": [],
            "id": user["_id"],
            "level": 2,
            "login": user["login"],
            "name": f"{user['firstName']} {user['lastName']}"
        }
    ],
}

try:
    collection = gc.createCollection("HTMAX", "HT-MAX Collection")
except Exception:
    collection = gc.get("/collection", parameters={"text": "HTMAX"})[0]

gc.put(f"/collection/{collection['_id']}/access", parameters={"access": json.dumps(access)})

xrd_folder = gc.createFolder(
    collection["_id"], "xrd_data", parentType="collection", reuseExisting=True
)
gc.put(f"/folder/{xrd_folder['_id']}/access", parameters={"access": json.dumps(access)})

depositions = [
    {
        "prefix": "JHBMAA",
        "metadata": {
            "titles": [{"title": "Pure Al foil"}],
            "alternateIdentifiers": [
                {
                    "alternateIdentifier": "Al20230428",
                    "alternateIdentifierType": "local",
                }
            ]
        },
    },
    {
        "prefix": "JHBMAA",
        "metadata": {
            "titles": [{"title": "Pure Al foil"}],
            "alternateIdentifiers": [
                {
                    "alternateIdentifier": "Al20250520",
                    "alternateIdentifierType": "local",
                }
            ]
        },
    },
]

for deposition in depositions:
    obj = gc.post(
        "deposition",
        parameters={
            "prefix": deposition["prefix"],
            "metadata": json.dumps(deposition["metadata"]),
        },
    )
    print(obj)
    # gc.put(f"deposition/{obj['_id']}/access", parameters={"access": json.dumps(access)})
    print("!!!!!!!!!!!!!!!!!!!!")

with open("power_supply_schema.json") as f:
    schema = json.load(f)

ps_form = gc.post(
    "form",
    data={"schema": json.dumps(schema)},
    parameters={
        "name": schema["title"],
        "description": schema["description"],
        "folderId": None,
        "pathTemplate": None,
        "entryFileName": None,
        "gdriveFolderId": None,
        "uniqueField": "name",
    },
)
gc.put(f"form/{ps_form['_id']}/access", parameters={"access": json.dumps(access)})

power_supplies = [
    {"name": "PS1", "manufacturer": "MDX", "power": 1.5, "serialNumber": "109992"},
    {"name": "PS2", "manufacturer": "MDX", "power": 1.5, "serialNumber": "109995"},
    {"name": "PS3", "manufacturer": "MDX", "power": 1.5, "serialNumber": "3175"},
    {"name": "PS4", "manufacturer": "MDX", "power": 2.5, "serialNumber": "139138"},
]
for power_supply in power_supplies:
    gc.post(
        "entry",
        parameters={
            "formId": ps_form["_id"],
            "data": json.dumps(power_supply),
        },
    )

with open("gun_schema.json") as f:
    schema = json.load(f)

gun_form = gc.post(
    "form",
    parameters={
        "name": schema["title"],
        "description": schema["description"],
        "schema": json.dumps(schema),
        "folderId": None,
        "pathTemplate": None,
        "entryFileName": None,
        "gdriveFolderId": None,
        "uniqueField": "name",
    },
)
gc.put(f"form/{gun_form['_id']}/access", parameters={"access": json.dumps(access)})
guns = [
    {
        "name": "Gun 1",
        "manufacturer": "MDX",
        "geometry": "Linear",
        "serialNumber": "123456",
        "gunType": "DC",
        "size": "Small",
    },
    {
        "name": "Gun 2",
        "manufacturer": "MDX",
        "geometry": "Round",
        "serialNumber": "654321",
        "gunType": "DC",
        "size": "Medium",
    },
    {
        "name": "Gun 3",
        "manufacturer": "MDX",
        "geometry": "Linear",
        "serialNumber": "789012",
        "gunType": "RF",
        "size": "Large",
    },
    {
        "name": "Gun 4",
        "manufacturer": "MDX",
        "geometry": "Linear",
        "serialNumber": "210987",
        "gunType": "DC",
        "size": "Small",
    },
    {
        "name": "Gun 5",
        "manufacturer": "Angstrom Sciences",
        "geometry": "Linear",
        "serialNumber": "",
        "gunType": "DC",
        "size": '5"x12"',
    },
]
for gun in guns:
    gc.post(
        "entry",
        parameters={
            "formId": gun_form["_id"],
            "data": json.dumps(gun),
        },
    )

with open("target_source_schema.json") as f:
    schema = json.load(f)
target_source_form = gc.post(
    "form",
    data={"schema": json.dumps(schema)},
    parameters={
        "name": schema["title"],
        "description": schema["description"],
        "folderId": None,
        "pathTemplate": None,
        "entryFileName": None,
        "gdriveFolderId": None,
        "jsHelpers": rjsmin.jsmin(open("target_source_schema.js", "r").read()),
        "uniqueField": "sampleId",
    },
)
gc.put(f"form/{target_source_form['_id']}/access", parameters={"access": json.dumps(access)})

depositions = gc.get("deposition")
elements = ["Al", "Al"]
for i, deposition in enumerate(depositions):
    element = elements[i]
    local_id = deposition["metadata"]["alternateIdentifiers"][0]["alternateIdentifier"]
    data = {
        "IGSN": deposition["igsn"],
        "contaminants": "",
        "depositionId": deposition["_id"],
        "element": element,
        "localId": local_id,
        "lookup": f"{deposition['igsn']} - {deposition['_id']} - ({local_id})",
        "manufacturer": "Process Materials",
        "purchaseOrder": "",
        "purity": 99.99,
        "sampleId": f"{deposition['igsn']} - {element} - ({local_id})",
    }
    gc.post(
        "entry",
        parameters={
            "formId": target_source_form["_id"],
            "data": json.dumps(data),
        },
    )

with open("target_schema.json") as f:
    schema = json.load(f)


source = (
    f"girder.formId:{target_source_form['_id']}"
    ":{entry[data][element]} - {entry[_id]}"
)
schema["properties"]["sources"]["items"]["properties"]["source"]["enumSource"] = source
target_form = gc.post(
    "form",
    data={"schema": json.dumps(schema)},
    parameters={
        "name": schema["title"],
        "description": schema["description"],
        "folderId": None,
        "pathTemplate": None,
        "entryFileName": None,
        "gdriveFolderId": None,
        "jsHelpers": rjsmin.jsmin(open("target_schema.js", "r").read()),
        "uniqueField": "name",
    },
)
gc.put(f"form/{target_form['_id']}/access", parameters={"access": json.dumps(access)})

with open("sputter_run_schema.json") as f:
    schema = json.load(f)

schema["definitions"]["sputter"]["properties"]["gun"][
    "enumSource"
] = f"girder.formId:{gun_form['_id']}"
schema["definitions"]["sputter"]["properties"]["target"][
    "enumSource"
] = f"girder.formId:{target_form['_id']}"
schema["definitions"]["sputter"]["properties"]["powerSupply"][
    "enumSource"
] = f"girder.formId:{ps_form['_id']}"

form = gc.post(
    "form",
    data={"schema": json.dumps(schema)},
    parameters={
        "name": schema["title"],
        "description": schema["description"],
        "folderId": None,
        "pathTemplate": None,
        "entryFileName": None,
        "gdriveFolderId": None,
        "jsHelpers": rjsmin.jsmin(open("sputter_run_schema.js", "r").read()),
        "uniqueField": "assignedIGSN",
    },
)
gc.put(f"form/{form['_id']}/access", parameters={"access": json.dumps(access)})

for fname in ["xrd_characterization.json", "sputter_characterization.json"]:
    with open(fname) as f:
        schema = json.load(f)

    js_helpers = None
    if os.path.isfile(fname[:-5] + ".js"):
        js_helpers = rjsmin.jsmin(open(fname[:-5] + ".js", "r").read())

    form = gc.post(
        "form",
        data={"schema": json.dumps(schema)},
        parameters={
            "name": schema["title"],
            "description": schema["description"],
            "folderId": xrd_folder["_id"],
            "pathTemplate": None,
            "entryFileName": None,
            "gdriveFolderId": None,
            "jsHelpers": js_helpers,
            "uniqueField": "assignedIGSN",
            "postEntryTask": "relate_entry_to_igsn(assignedIGSN)",
        },
    )
    gc.put(f"form/{form['_id']}/access", parameters={"access": json.dumps(access)})
