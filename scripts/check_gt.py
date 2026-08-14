import json

with open("backend/evaluation/datasets/hotpotqa_benchmark_v1.json") as f:
    data = json.load(f)

for item in data:
    if item["id"] == "5adfa059554299025d62a2f8":
        print(f"RAW JSON RECORD for 5adfa059554299025d62a2f8:\n{json.dumps(item, indent=2)}")
        break

print("\n\nChecking next 15 records to see if answers align with questions:")
for item in data[:15]:
    print(f"Q: {item['question']}")
    print(f"A: {item['answer']}")
    print("-" * 50)
