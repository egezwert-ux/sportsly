import requests
from bs4 import BeautifulSoup
from datetime import datetime

FIXTURE_URL = "FIXTURE_URL_BURAYA"
RESULT_URL = "RESULT_URL_BURAYA"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_today_fixtures():

    r = requests.get(FIXTURE_URL, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    fixtures = []

    matches = soup.select("MATCH_SELECTOR_BURAYA")

    for m in matches:

        home = m.select_one("HOME_SELECTOR")
        away = m.select_one("AWAY_SELECTOR")
        time = m.select_one("TIME_SELECTOR")

        if not home or not away:
            continue

        fixtures.append({
            "id": str(hash(home.text + away.text)),
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "time": time.text.strip() if time else "00:00",
            "league": "Unknown",
            "homeTeam": home.text.strip(),
            "awayTeam": away.text.strip()
        })

    return fixtures


def fetch_today_results():

    r = requests.get(RESULT_URL, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    results = []

    matches = soup.select("RESULT_MATCH_SELECTOR")

    for m in matches:

        home = m.select_one("RESULT_HOME_SELECTOR")
        away = m.select_one("RESULT_AWAY_SELECTOR")
        score = m.select_one("RESULT_SCORE_SELECTOR")

        if not home or not away or not score:
            continue

        results.append({
            "id": str(hash(home.text + away.text)),
            "score": score.text.strip()
        })

    return results
