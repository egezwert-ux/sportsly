import json
from datetime import datetime
from helpers import fetch_today_fixtures

JSON_PATH = "docs/predictions.json"

def update_results():
    try:
        with open(JSON_PATH, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"lastUpdated": str(datetime.utcnow()), "matches": []}

    fixtures = fetch_today_fixtures()
    for match in fixtures:
        for m in data["matches"]:
            if m["id"] == match["id"]:
                # Örnek placeholder: Sofascore’dan gerçek sonuçları buraya ekleyebilirsin
                m["result"] = "update_needed"
    with open(JSON_PATH, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    update_results()
