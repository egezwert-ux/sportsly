import os
import json
from datetime import datetime
from helpers import fetch_today_fixtures
import requests

JSON_PATH = "docs/predictions.json"
GEMINI_KEY = os.getenv("GEMINI_KEY")
AI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

def ai_predict(home, away):
    prompt = f"Predict for {home} vs {away} in JSON with mainPick, odds, confidence, predictedScore, btts, corners, cards, htFt, analysis"
    payload = {"contents":[{"parts":[{"text": prompt}]}]}
    headers = {"Authorization": f"Bearer {GEMINI_KEY}"}
    try:
        r = requests.post(AI_URL, json=payload, headers=headers, timeout=15)
        r.raise_for_status()
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text)
    except Exception as e:
        print("AI prediction failed:", e)
        return {}

def generate_predictions():
    fixtures = fetch_today_fixtures()
    predictions = []
    for match in fixtures:
        pred = ai_predict(match["homeTeam"], match["awayTeam"])
        predictions.append({
            "id": match["id"],
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
