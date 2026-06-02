import json

with open("../datasets/debug_dataset.json", "r") as f:
    data = json.load(f)

print("Total Samples:", len(data))

print("\nFirst Example:\n")
print(data[0])