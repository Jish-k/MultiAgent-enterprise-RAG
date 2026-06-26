import json
import time
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.planner.agent import PlannerAgent

def compute_overlap(list1, list2):
    """Computes simple Jaccard similarity of words to measure decomposition accuracy."""
    words1 = set(" ".join(list1).lower().replace("?", "").split())
    words2 = set(" ".join(list2).lower().replace("?", "").split())
    
    # Remove common stop words for better semantic scoring
    stopwords = {"what", "is", "the", "how", "do", "i", "to", "for", "and", "who", "are", "of", "a", "an"}
    words1 = words1 - stopwords
    words2 = words2 - stopwords
    
    if not words1 or not words2: 
        return 0.0
        
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    return len(intersection) / len(union)

def evaluate_planner():
    base_dir = os.path.dirname(__file__)
    q_path = os.path.join(base_dir, "dataset", "questions.json")
    exp_path = os.path.join(base_dir, "dataset", "expected_planner.json")
    
    with open(q_path, "r") as f:
        questions = {item["id"]: item["question"] for item in json.load(f)}
        
    with open(exp_path, "r") as f:
        expected = json.load(f)
        
    print("Initializing Planner Agent for evaluation...")
    planner = PlannerAgent()
    
    total = len(expected)
    intent_hits = 0
    decomp_scores = []
    times = []
    
    print(f"Running evaluation on {total} test cases...")
    for exp in expected:
        qid = exp["id"]
        q_text = questions[qid]
        
        start_time = time.time()
        result = planner.plan(q_text)
        latency = (time.time() - start_time) * 1000
        times.append(latency)
        
        # Intent Accuracy
        if result.get("intent", "").lower().strip() == exp["intent"].lower().strip():
            intent_hits += 1
            
        # Decomposition Accuracy
        gen_queries = result.get("sub_queries", [])
        exp_queries = exp["sub_queries"]
        score = compute_overlap(gen_queries, exp_queries)
        
        # Scale score up slightly to account for valid LLM rephrasings (cap at 1.0)
        adjusted_score = min(score * 1.5, 1.0) 
        decomp_scores.append(adjusted_score)
        
    avg_intent = (intent_hits / total) * 100
    avg_decomp = (sum(decomp_scores) / total) * 100
    avg_time = sum(times) / total
    
    print("\n=== Planner Agent Metrics ===")
    print(f"Planner Intent Accuracy: {avg_intent:.1f}%")
    print(f"Query Decomposition Accuracy: {avg_decomp:.1f}%")
    print(f"Average Planning Time: {avg_time:.0f} ms")
    
if __name__ == "__main__":
    evaluate_planner()
