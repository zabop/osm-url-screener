from requests_oauthlib import OAuth2Session
import requests
import random
import osmapi
import json

token = {
    "access_token": "MQtTb5U9BslGtnFoApnSPwgKoqEsFgCTKVWWXw2fyYo",
    "token_type": "Bearer",
}

client_id = "PEZADPwzYY225tBhbTvI_uqdZpvdYMZzDhulVCG0Fyg"
oauth_session = OAuth2Session(token=token)
api = osmapi.OsmApi(api="https://api.openstreetmap.org", session=oauth_session)

localities = [
    10187,
    28595,
    51800,
    57032,
    57397,
    57398,
    57516,
    57533,
    57534,
    57535,
    57537,
    57539,
    57581,
    57582,
    60148,
    69361,
    72894,
    76155,
    76489,
    76521,
    77904,
    78312,
    80277,
    81941,
    82631,
    85103,
    87944,
    88066,
    88067,
    88068,
    88070,
    88081,
    88083,
    89846,
    92650,
    99774,
    103776,
    107240,
    110212,
    111014,
    113682,
    113757,
    114085,
    114311,
    115074,
    116938,
    117097,
    123292,
    127167,
    127864,
    134324,
    134353,
    137981,
    142308,
    147278,
    147284,
    148603,
    148780,
    150988,
    150989,
    150994,
    153375,
    153377,
    153487,
    153488,
    154350,
    158019,
    158039,
    158392,
    158396,
    161640,
    161643,
    161649,
    162353,
    163183,
    167058,
    167060,
    172385,
    172504,
    172799,
    180837,
    180904,
    181040,
    189890,
    189924,
    190380,
    192442,
    195384,
    195444,
    198566,
    283679,
    297286,
    297287,
    298793,
    335184,
    358021,
    375982,
    1433249,
    1625787,
    1763195,
    1775685,
    1775792,
    1877232,
    1900654,
    1900655,
    1905258,
    1905841,
    1906767,
    1910014,
    1910704,
    1915429,
    1919950,
    1920242,
    1920348,
    1920349,
    1920584,
    1920660,
    1920841,
    1920842,
    1920901,
    1920902,
    1920903,
    1921172,
    1921173,
    1921238,
    1921239,
    1921240,
    1921241,
    1959008,
    2235077,
    2750460,
    2750598,
    2750677,
    2750939,
    2751428,
    9448448,
    9448449,
    10792351,
    10792352,
    10947197,
    15684264,
    15684265,
]


def get_nwr(relid):

    url = f"https://osm-url-screener.zabop.workers.dev/{relid}"
    print(url)

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

    return nodes, ways, relations


for _ in range(10):
    nodes, ways, relations = get_nwr(random.choice(localities))
    if len(nodes) + len(ways) + len(relations) > 0:
        break
else:
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
