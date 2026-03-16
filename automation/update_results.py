import json
from helpers import fetch_today_results

JSON_PATH = "docs/predictions.json"

def update_results():
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Predictions file not found!")
        return

    results = fetch_today_results()
    for m in data.get("matches", []):
        for r in results:
            if r["id"] == m["id"]:
                if r["score"]:
                    m["result"] = "won" if r["score"] == m["prediction"].get("predictedScore") else "lost"

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    update_results()
