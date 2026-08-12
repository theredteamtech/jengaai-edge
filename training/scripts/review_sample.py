import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

TRAIN = ROOT / "training/data/jengacoder_train_v1.json"

random.seed(42)

with TRAIN.open("r", encoding="utf-8") as f:
    data = json.load(f)

keywords = {
    "Arduino": ["arduino", "hc-sr04", "servo"],
    "Kiswahili": ["kiswahili", "mwanafunzi", "elezea"],
    "Debugging": ["fix", "debug", "correct"],
    "General coding": ["python", "fastapi", "javascript"],
}

selected = []
used = set()

targets = {
    "Arduino": 8,
    "Kiswahili": 5,
    "Debugging": 3,
    "General coding": 4,
}

for category, words in keywords.items():
    candidates = []

    for index, item in enumerate(data):
        if index in used:
            continue

        text = (
            item["system"]
            + " "
            + item["instruction"]
            + " "
            + item.get("input", "")
        ).lower()

        if any(word in text for word in words):
            candidates.append((index, item))

    random.shuffle(candidates)

    for index, item in candidates[:targets[category]]:
        used.add(index)
        selected.append((category, index, item))

for number, (category, index, item) in enumerate(selected, 1):
    print("\n" + "=" * 90)
    print(f"REVIEW {number} | {category} | dataset index {index}")
    print("=" * 90)

    print("\nSYSTEM:")
    print(item["system"])

    print("\nINSTRUCTION:")
    print(item["instruction"])

    if item.get("input"):
        print("\nINPUT:")
        print(item["input"])

    print("\nOUTPUT:")
    print(item["output"])

print("\n" + "=" * 90)
print(f"TOTAL REVIEWED: {len(selected)}")
print("=" * 90)
