from db import debug_history
import json

records = list(debug_history.find())

dataset = []

for r in records:
    if (
        "buggy_code" in r and
        "fixed_code" in r and
        "explanation" in r
    ):
        dataset.append({
            "buggy_code": r["buggy_code"],
            "fixed_code": r["fixed_code"],
            "explanation": r["explanation"]
        })

with open("../datasets/debug_dataset.json", "w") as f:
    json.dump(dataset, f, indent=2)

print(f"Exported {len(dataset)} examples")