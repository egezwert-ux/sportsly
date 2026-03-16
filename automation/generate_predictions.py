# generate_predictions.py
import json
import os
import requests
from datetime import datetime
from helpers import fetch_today_fixtures

AI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
AI_KEY = os.environ.get("GEMINI_KEY")  # secret environment variable

JSON_PATH = "docs/predictions.json"

def ai_predict(home, away):
    prompt = (
        f"Predict for {home} vs {away} in JSON with mainPick, odds, confidence, "
        "predictedScore, btts, corners, cards, htFt, analysis"
    )
    payload = {"contents":[{"parts":[{"text": prompt}]}]}
    headers = {"Authorization": f"Bearer {AI_KEY}"}

    try:
        r = requests.post(AI_URL, json=payload, headers=headers)
        r.raise_for_status()
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text)
    except Exception as e:
        print(f"AI tahmin hatası: {e}")
        return {
            "mainPick": "",
            "odds": "",
            "confidence": 0,
            "predictedScore": "",
            "btts": "",
            "corners": "",
            "cards": "",
            "htFt": "",
            "analysis": ""
        }

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

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump({"lastUpdated": str(datetime.utcnow()), "matches": predictions}, f, indent=4, ensure_ascii=False)
    print(f"{len(predictions)} tahmin oluşturuldu ve {JSON_PATH} dosyasına kaydedildi.")

if __name__ == "__main__":
    generate_predictions()
