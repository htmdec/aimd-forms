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
for deposition in gc.get("deposition"):
    gc.delete("deposition/%s" % deposition["_id"])

depositions = [
    {
        "prefix": "JHAMAL",
        "metadata": {
            "titles": [{"title": "Pure Nb foil"}],
        },
    },
    {
        "prefix": "JHAMAL",
        "metadata": {
            "titles": [{"title": "Pure Ti foil"}],
        },
    },
]

for deposition in depositions:
    gc.post(
        "deposition",
        parameters={
            "prefix": deposition["prefix"],
            "metadata": json.dumps(deposition["metadata"]),
        },
    )

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
guns = [
    {
        "name": "Gun 1",
        "manufacturer": "MDX",
        "geometry": "Linear",
        "serialNumber": "123456",
        "gunType": "Gun Type 1",
        "size": "Small",
    },
    {
        "name": "Gun 2",
        "manufacturer": "MDX",
        "geometry": "Round",
        "serialNumber": "654321",
        "gunType": "Gun Type 2",
        "size": "Medium",
    },
    {
        "name": "Gun 3",
        "manufacturer": "MDX",
        "geometry": "Linear",
        "serialNumber": "789012",
        "gunType": "Gun Type 3",
        "size": "Large",
    },
    {
        "name": "Gun 4",
        "manufacturer": "MDX",
        "geometry": "Linear",
        "serialNumber": "210987",
        "gunType": "Gun Type 1",
        "size": "Small",
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

depositions = gc.get("deposition")
elements = ["Nb", "Ti", "Fe", "Cl"]
for i, deposition in enumerate(depositions):
    element = elements[i]
    data = {
        "IGSN": deposition["igsn"],
        "contaminants": "S, Fe, Cl",
        "depositionId": deposition["_id"],
        "element": element,
        "lookup": f"{deposition['igsn']} - {deposition['_id']}",
        "manufacturer": "MDX",
        "purchaseOrder": "https://foo.com/1234",
        "purity": 99.99,
        "sampleId": f"{deposition['igsn']} - {element}",
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
