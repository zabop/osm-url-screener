from requests_oauthlib import OAuth2Session
import requests
import osmapi
import json

token = {
    "access_token": "MQtTb5U9BslGtnFoApnSPwgKoqEsFgCTKVWWXw2fyYo",
    "token_type": "Bearer",
}

client_id = "PEZADPwzYY225tBhbTvI_uqdZpvdYMZzDhulVCG0Fyg"
oauth_session = OAuth2Session(token=token)
api = osmapi.OsmApi(api="https://api.openstreetmap.org", session=oauth_session)

url = "https://osm-url-screener.zabop.workers.dev/11559909"
with open("cfresp.json", "wb") as f:
    f.write(requests.get(url).content)

with open("cfresp.json", "r") as f:
    cfresp = json.load(f)

nodes, ways, relations = [], [], []
for feature in cfresp["resp404"].keys():
    if feature.startswith("n"):
        nodes.append(int(feature[1:]))
    elif feature.startswith("w"):
        ways.append(int(feature[1:]))
    elif feature.startswith("r"):
        relations.append(int(feature[1:]))

if len(nodes) + len(ways) + len(relations) == 0:
    print("No 404s found")
    exit()

plural = ""
if len(nodes) + len(ways) + len(relations) > 1:
    plural += "s"

with api.Changeset(
    {"comment": f"remove 404-returning website{plural}"}
) as changeset_id:

    for node in nodes:
        f = api.NodeGet(node)
        try:
            del f["tag"]["contact:website"]
        except KeyError:
            print("Website removed in the meantime")
        else:
            api.NodeUpdate(f)

    for way in ways:
        f = api.WayGet(way)
        try:
            del f["tag"]["contact:website"]
        except KeyError:
            print("Website removed in the meantime")
        else:
            api.WayUpdate(f)

    for relation in relations:
        f = api.WayGet(relation)
        try:
            del f["tag"]["contact:website"]
        except KeyError:
            print("Website removed in the meantime")
        else:
            api.RelationUpdate(f)
