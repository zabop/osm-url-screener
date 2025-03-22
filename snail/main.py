import random
import requests
import json

ids = [51806, 51906, 51781, 184724, 51831]

selected_id = random.choice(ids)
url = f"https://osm-url-screener.zabop.workers.dev/{selected_id}"
response = requests.get(url)

with open(f"response_{selected_id}.json", "w") as f:
    json.dump(response.json(), f)
