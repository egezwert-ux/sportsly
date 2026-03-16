import soccerdata as sd
import json
from datetime import datetime

print("Fetching fixtures...")

sofa = sd.Sofascore()

schedule = sofa.read_schedule()

matches = []

for index, row in schedule.iterrows():
    matches.append({
        "id": str(index),
        "date": str(row.get("date","")),
        "league": str(row.get("league","")),
        "homeTeam": str(row.get("home_team","")),
        "awayTeam": str(row.get("away_team","")),
        "prediction": {},
        "result": "pending"
    })

data = {
    "lastUpdated": str(datetime.utcnow()),
    "matches": matches
}

with open("docs/predictions.json","w") as f:
    json.dump(data,f,indent=4)

print("Fixtures saved")
