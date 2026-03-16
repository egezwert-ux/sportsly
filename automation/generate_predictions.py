# generate_predictions.py
import json
import os
from datetime import datetime
from helpers import fetch_today_fixtures

import requests

AI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
AI_KEY = os.getenv("AI_KEY")  # Workflow’dan gelen secret
JSON_PATH = "docs/predictions.json"

def ai_predict(home, away):
    prompt = f"Predict for {home} vs {away} in JSON with mainPick, odds, confidence, predictedScore, btts, corners, cards, htFt, analysis"
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
        json.dump({"lastUpdated": str(datetime.utcnow()), "matches": predictions}, f, indent=4)

if __name__ == "__main__":
    generate_predictions()
