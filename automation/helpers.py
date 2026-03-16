# helpers.py
import requests
from datetime import datetime

# Sofascore API örnek endpoint
FIXTURE_URL = "https://api.sofascore.com/api/v1/sport/football/scheduled-events/{date}"
RESULTS_URL = "https://api.sofascore.com/api/v1/sport/football/scheduled-events/{date}"

def fetch_today_fixtures():
    date = datetime.utcnow().strftime("%Y-%m-%d")
    url = FIXTURE_URL.format(date=date)
    resp = requests.get(url)
    data = resp.json()

    fixtures = []
    for ev in data.get("events", []):
        fixtures.append({
            "id": str(ev.get("id")),
            "league": ev.get("tournament", {}).get("name"),
            "homeTeam": ev.get("homeTeam", {}).get("name"),
            "awayTeam": ev.get("awayTeam", {}).get("name"),
            "date": date
        })
    return fixtures

def fetch_today_results():
    date = datetime.utcnow().strftime("%Y-%m-%d")
    url = RESULTS_URL.format(date=date)
    resp = requests.get(url)
    data = resp.json()

    results = []
    for ev in data.get("events", []):
        score_home = ev.get("homeScore", 0)
        score_away = ev.get("awayScore", 0)
        results.append({
            "id": str(ev.get("id")),
            "score": f"{score_home}-{score_away}"
        })
    return results
