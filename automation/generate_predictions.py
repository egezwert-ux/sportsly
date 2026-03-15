import json
import requests
from datetime import datetime
from helpers import fetch_today_fixtures

# Gemini AI endpoint ve key (buraya kendi key’ini koy)
AI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
AI_KEY = "YOUR_GEMINI_API_KEY"  # buraya kendi key’ini ekle

JSON_PATH = "docs/predictions.json"

def ai_predict(home, away):
    prompt = f"Predict {home} vs {away} with mainPick, odds, confidence, predictedScore, btts, corners, cards, htFt, analysis in JSON"
    payload = {"contents":[{"parts":[{"text": prompt}]}]}
    headers = {"Authorization": f"Bearer {AI_KEY}"}
    r = requests.post(AI_URL, json=payload, headers=headers)
    text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(text)

def generate_predictions():
    fixtures = fetch_today_fixtures()
    predictions = []

    for match in fixtures:
        home = match["homeTeam"]
        away = match["awayTeam"]
        pred = ai_predict(home, away)

        predictions.append({
            "id": str(match["id"]),
            "date": match["date"],
            "league": match["league"],
            "homeTeam": home,
            "awayTeam": away,
            "prediction": pred,
            "analysis": pred.get("analysis", ""),
            "result": "pending",
            "vip": False,
            "adUnlock": True
        })

    with open(JSON_PATH, "w") as f:
        json.dump({"lastUpdated": str(datetime.utcnow().date()), "matches": predictions}, f, indent=4)

if name == "main":
    generate_predictions()
