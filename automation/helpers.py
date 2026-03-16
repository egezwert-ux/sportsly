# helpers.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_today_fixtures():
    url = "https://www.sofascore.com/football/fixtures"  # sen burayı kendi endpoint ile değiştireceksin
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    fixtures = []

    # Selector örneği (sen kendi sayfa elementlerine göre değiştir)
    for tr in soup.select("tr.match"):
        home = tr.select_one(".home")
        away = tr.select_one(".away")
        if not home or not away:
            continue
        fixtures.append({
            "id": tr.get("data-id"),
            "league": tr.get("data-league"),
            "homeTeam": home.text.strip(),
            "awayTeam": away.text.strip(),
            "date": datetime.utcnow().strftime("%Y-%m-%d")
        })
    return fixtures

def fetch_today_results():
    url = "https://www.sofascore.com/football/results"  # kendi endpoint ile değiştir
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []

    for tr in soup.select("tr.match"):
        match_id = tr.get("data-id")
        score = tr.select_one(".score").text.strip() if tr.select_one(".score") else None
        results.append({"id": match_id, "score": score})
    return results
