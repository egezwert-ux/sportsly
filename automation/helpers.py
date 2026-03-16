import requests
from datetime import datetime

# Sofascore scheduled events endpoint (örnek)
FIXTURE_URL = "https://api.sofascore.com/api/v1/sport/football/scheduled-events/{date}"
RESULTS_URL = "https://api.sofascore.com/api/v1/sport/football/live-events"

def fetch_today_fixtures():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    url = FIXTURE_URL.format(date=today)
    headers = {"User-Agent": "Mozilla/5.0"}
    
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    
    fixtures = []
    for event in data.get("events", []):
        fixtures.append({
            "id": event.get("id"),
            "league": event.get("tournament", {}).get("name"),
            "homeTeam": event.get("homeTeam", {}).get("name"),
            "awayTeam": event.get("awayTeam", {}).get("name"),
            "date": today
        })
    return fixtures

def fetch_today_results():
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(RESULTS_URL, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    
    results = []
    for event in data.get("events", []):
        results.append({
            "id": event.get("id"),
            "score": f"{event.get('homeScore',0)}-{event.get('awayScore',0)}"
        })
    return results
