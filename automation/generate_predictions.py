import json
import random

print("Generating predictions...")

with open("docs/predictions.json","r") as f:
    data = json.load(f)

for match in data["matches"]:

    match["prediction"] = {
        "mainPick": random.choice(["MS 1","MS X","MS 2"]),
        "confidence": random.randint(55,80),
        "predictedScore": random.choice(["1-0","1-1","2-1","0-1"]),
        "btts": random.choice(["KG VAR","KG YOK"]),
        "corners": random.choice(["8.5 ÜST","8.5 ALT"])
    }

with open("docs/predictions.json","w") as f:
    json.dump(data,f,indent=4)

print("Predictions generated")
