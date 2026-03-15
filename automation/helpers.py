def fetch_today_fixtures():
    url = "https://www.flashscore.com/today-fixtures"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    fixtures = []

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
