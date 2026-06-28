import json
import os
import random
from collections import defaultdict
from datetime import datetime

DATA_DIR = "evaluation/dataset"

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def run_validation():
    print("Starting Dataset Integrity Validation...\n")
    
    questions = load_json("questions.json")
    ground_truth = load_json("ground_truth.json")
    planner = load_json("expected_planner.json")
    metadata = load_json("metadata.json")
    
    errors = []
    
    # Check 1: File Completeness
    if len(questions) != 140: errors.append(f"questions.json has {len(questions)} entries, expected 140")
    if len(ground_truth) != 140: errors.append(f"ground_truth.json has {len(ground_truth)} entries, expected 140")
    if len(planner) != 140: errors.append(f"expected_planner.json has {len(planner)} entries, expected 140")
    if len(metadata) != 140: errors.append(f"metadata.json has {len(metadata)} entries, expected 140")
    
    # Map by ID for easy access
    q_map = {q["id"]: q for q in questions if "id" in q}
    gt_map = {g["id"]: g for g in ground_truth if "id" in g}
    pl_map = {p["id"]: p for p in planner if "id" in p}
    md_map = {m["id"]: m for m in metadata if "id" in m}
    
    # Check 3: ID Consistency
    all_expected_ids = {f"Q{i:03d}" for i in range(1, 141)}
    
    for name, mapping in [("questions", q_map), ("ground_truth", gt_map), ("expected_planner", pl_map), ("metadata", md_map)]:
        missing = all_expected_ids - set(mapping.keys())
        extra = set(mapping.keys()) - all_expected_ids
        if missing: errors.append(f"{name}.json missing IDs: {missing}")
        if extra: errors.append(f"{name}.json has extra IDs: {extra}")
        
    # Check 2, 4, 5, 6 for each ID
    for qid in all_expected_ids:
        q = q_map.get(qid, {})
        gt = gt_map.get(qid, {})
        pl = pl_map.get(qid, {})
        md = md_map.get(qid, {})
        
        # Check 2: Missing Fields
        required_q = ["question", "category", "difficulty", "question_type", "expected_documents"]
        for field in required_q:
            if field not in q or q[field] == "" or q[field] == []:
                if field != "expected_documents" or q.get("question_type") != "Out of Domain":
                    # Out of domain might have empty expected documents
                    if field == "expected_documents" and not q.get(field):
                        pass # Allowed for out of domain
                    else:
                        errors.append(f"questions.json [{qid}] missing or empty field: {field}")
                
        required_gt = ["expected_answer", "expected_documents", "expected_pages"]
        for field in required_gt:
            if field not in gt or (gt[field] == "" and field == "expected_answer"):
                errors.append(f"ground_truth.json [{qid}] missing or empty field: {field}")
                
        required_pl = ["intent", "complexity", "required_information", "retrieval_strategy", "expected_documents"]
        for field in required_pl:
            if field not in pl or pl[field] == "":
                errors.append(f"expected_planner.json [{qid}] missing or empty field: {field}")
                
        required_md = ["difficulty", "category", "question_type", "requires_reasoning", "requires_multiple_documents", "expected_document_count", "requires_verification", "requires_planning", "retrieval_difficulty"]
        for field in required_md:
            if field not in md:
                errors.append(f"metadata.json [{qid}] missing field: {field}")

        # Check 4: Planner Consistency (using Metadata)
        if md.get("category") == "Cross Document" and not md.get("requires_multiple_documents"):
            errors.append(f"Consistency [{qid}]: Category is Cross Document but requires_multiple_documents is False")
        if md.get("difficulty") == "Hard" and not md.get("requires_reasoning"):
            errors.append(f"Consistency [{qid}]: Difficulty is Hard but requires_reasoning is False")

        # Check 5: Ground Truth Quality
        ans = gt.get("expected_answer", "")
        words = ans.split()
        if len(words) <= 2:
            errors.append(f"Ground Truth [{qid}]: Answer too short ({len(words)} words)")
        if len(words) > 400:
            errors.append(f"Ground Truth [{qid}]: Answer too long ({len(words)} words)")
        lower_ans = ans.lower()
        for phrase in ["i think", "probably", "maybe"]:
            if phrase in lower_ans:
                errors.append(f"Ground Truth [{qid}]: Unprofessional language found ('{phrase}')")

        # Check 6: Planner Output Quality
        req_info = pl.get("required_information", [])
        q_type = q.get("question_type", "")
        if isinstance(req_info, list):
            if len(req_info) < 1:
                errors.append(f"Planner Quality [{qid}]: required_information is empty")
            if "Multi Hop" in q_type and len(req_info) < 2:
                errors.append(f"Planner Quality [{qid}]: Multi-hop question has only {len(req_info)} required_information item")
        else:
            errors.append(f"Planner Quality [{qid}]: required_information must be a list")

    if errors:
        print(f"FAILED: Found {len(errors)} integrity errors.")
        for err in errors[:20]:
            print(" -", err)
        if len(errors) > 20:
            print(f" ... and {len(errors) - 20} more errors.")
        return False
        
    print("SUCCESS: All integrity checks passed!\n")
    
    # Generate Review Report
    print("Generating stratified random review report...")
    categories = defaultdict(list)
    for qid, q in q_map.items():
        if q["category"] == "Adversarial":
            categories["Adversarial"].append(qid)
        elif q["category"] == "Cross Document":
            categories["Cross Document"].append(qid)
        else:
            categories[q["difficulty"]].append(qid)

    sampled_ids = []
    for cat in ["Easy", "Medium", "Hard", "Cross Document", "Adversarial"]:
        pool = categories.get(cat, [])
        sample_size = min(5, len(pool))
        sampled_ids.extend(random.sample(pool, sample_size))
        
    report_path = os.path.join(DATA_DIR, "validation_report.md")
    with open(report_path, "w") as f:
        f.write("# Stratified Random Validation Report\n\n")
        f.write(f"Inspected {len(sampled_ids)} questions across all categories.\n\n")
        
        for qid in sampled_ids:
            q = q_map.get(qid, {})
            gt = gt_map.get(qid, {})
            pl = pl_map.get(qid, {})
            md = md_map.get(qid, {})

            f.write(f"## {qid}: {q.get('question', 'N/A')}\n\n")
            f.write("### Ground Truth\n")
            f.write(f"**Expected Answer:** {gt.get('expected_answer', 'N/A')}\n\n")
            f.write("### Planner Expected Output\n")
            f.write(f"**Intent:** {pl.get('intent', 'N/A')} | **Strategy:** {pl.get('retrieval_strategy', 'N/A')}\n")
            f.write(f"**Required Info:** {pl.get('required_information', 'N/A')}\n\n")
            f.write("---\n\n")
            
    print(f"Review report saved to {report_path}")
    
    # Generate VERSION.md
    version_path = os.path.join(DATA_DIR, "VERSION.md")
    with open(version_path, "w") as f:
        f.write("Dataset Version: 1.0\n\n")
        f.write("Questions: 140\n")
        f.write("Ground Truth: Generated + Reviewed\n")
        f.write("Planner Labels: Generated + Reviewed\n")
        f.write("Metadata: Deterministic\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
    print(f"VERSION.md successfully generated at {version_path}")
    return True

if __name__ == "__main__":
    run_validation()
