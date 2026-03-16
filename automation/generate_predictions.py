import json
import requests
from datetime import datetime
from helpers import fetch_today_fixtures

# AI Gemini API URL ve secret
AI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
JSON_PATH = "docs/predictions.json"

def ai_predict(home, away, api_key):
    prompt = f"Predict for {home} vs {away} in JSON with mainPick, odds, confidence, predictedScore, btts, corners, cards, htFt, analysis"
    payload = {"contents":[{"parts":[{"text": prompt}]}]}
    headers = {"Authorization": f"Bearer {api_key}"}
    r = requests.post(AI_URL, json=payload, headers=headers)
    text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(text)

def generate_predictions(api_key):
    fixtures = fetch_today_fixtures()
    predictions = []

    for match in fixtures:
        pred = ai_predict(match["homeTeam"], match["awayTeam"], api_key)
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
    import os
    api_key = os.environ.get("GEMINI_KEY")
    generate_predictions(api_key)
