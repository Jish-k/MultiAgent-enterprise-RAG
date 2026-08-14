import json
import os
import random

def load_json(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        return json.load(f)

def generate_pilot():
    questions = {q["id"]: q for q in load_json("evaluation/dataset/questions.json")}
    
    if not questions:
        print("Questions dataset missing.")
        return

    distribution = {
        "Employee Handbook": 3,
        "Leave Policy": 3,
        "HR Policy": 3,
        "IT Security": 3,
        "Travel Policy": 2,
        "Expense Policy": 2,
        "Cross Document": 2,
        "Adversarial": 2
    }

    categories = {k: [] for k in distribution.keys()}
    for qid, q in questions.items():
        cat = q.get("category", "")
        if cat in categories:
            categories[cat].append(qid)

    pilot = []
    
    for cat, count in distribution.items():
        pool = categories[cat]
        sampled = random.sample(pool, count) if len(pool) >= count else pool
        for qid in sampled:
            pilot.append(questions[qid])

    out_path = "evaluation/dataset/pilot_questions.json"
    with open(out_path, "w") as f:
        json.dump(pilot, f, indent=2)
        
    print(f"Generated Pilot subset with {len(pilot)} questions at {out_path}.")

if __name__ == "__main__":
    generate_pilot()
