import os
import json
import requests
from datetime import datetime
from helpers import fetch_today_fixtures

JSON_PATH = "docs/predictions.json"
AI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
AI_KEY = os.environ.get("GEMINI_KEY")  # secret üzerinden çekilecek

def ai_predict(home, away):
    prompt = f"Predict {home} vs {away} in JSON with mainPick, odds, confidence, predictedScore, btts, corners, cards, htFt, analysis"
    payload = {"contents":[{"parts":[{"text": prompt}]}]}
    headers = {"Authorization": f"Bearer {AI_KEY}"}
    
    r = requests.post(AI_URL, json=payload, headers=headers)
    r.raise_for_status()
    text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(text)

def generate_predictions():
    fixtures = fetch_today_fixtures()
    predictions = []

    for match in fixtures:
        pred = ai_predict(match["homeTeam"], match["awayTeam"])
        predictions.append({
            "id": str(match["id"]),
            "date": match["date"],
            "league": match["league"],
            "homeTeam": match["homeTeam"],
            "awayTeam": match["awayTeam"],
            "prediction": pred,
            "analysis": pred.get("analysis", ""),
            "result": "pending",
            "vip": False,
            "adUnlock": True
        })

    with open(JSON_PATH, "w") as f:
        json.dump({"lastUpdated": str(datetime.utcnow()), "matches": predictions}, f, indent=4)

if __name__ == "__main__":
    generate_predictions()
