# automation/generate_predictions.py

import json
from datetime import datetime

# Boş tahmin üretim iskeleti
def generate_predictions():
    predictions = {
        "lastUpdated": str(datetime.utcnow().date()),
        "matches": []
    }
    # Buraya AI tahmin üretme kodu eklenecek
    # Örn: mainPick, odds, confidence, predictedScore vb.

    # JSON'u kaydet
    with open("docs/predictions.json", "w") as f:
        json.dump(predictions, f, indent=4)

if __name__ == "__main__":
    generate_predictions()
