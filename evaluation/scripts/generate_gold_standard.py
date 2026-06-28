import json
import os
import random

def load_json(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        return json.load(f)

def generate_gold_standard():
    questions = {q["id"]: q for q in load_json("evaluation/dataset/questions.json")}
    ground_truth = {q["id"]: q for q in load_json("evaluation/dataset/ground_truth.json")}
    
    if not questions or not ground_truth:
        print("Questions or Ground Truth dataset missing.")
        return

    distribution = {
        "Employee Handbook": 3,
        "Leave Policy": 3,
        "HR Policy": 3,
        "IT Security": 3,
        "Travel Policy": 3,
        "Cross Document": 5,
        "Adversarial": 5
    }

    # Group by category
    categories = {k: [] for k in distribution.keys()}
    for qid, q in questions.items():
        cat = q.get("category", "")
        if cat in categories:
            categories[cat].append(qid)

    gold_standard = []
    
    for cat, count in distribution.items():
        pool = categories[cat]
        if len(pool) < count:
            print(f"Warning: Not enough questions in category '{cat}'. Expected {count}, found {len(pool)}.")
            sampled = pool
        else:
            sampled = random.sample(pool, count)
            
        for qid in sampled:
            q = questions[qid]
            gt = ground_truth.get(qid, {})
            
            entry = {
                "id": qid,
                "question": q.get("question", ""),
                "category": cat,
                "expected_answer": gt.get("expected_answer", ""),
                "expected_documents": gt.get("expected_documents", []),
                "verification_status": "Human Verified"
            }
            gold_standard.append(entry)

    os.makedirs("evaluation/gold_standard", exist_ok=True)
    out_path = "evaluation/gold_standard/gold_standard.json"
    
    with open(out_path, "w") as f:
        json.dump(gold_standard, f, indent=2)
        
    print(f"Generated Gold Standard subset with {len(gold_standard)} verified questions at {out_path}.")

if __name__ == "__main__":
    generate_gold_standard()
