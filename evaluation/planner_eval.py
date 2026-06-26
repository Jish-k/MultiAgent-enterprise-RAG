import json
import time
import os
import sys
import numpy as np

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.planner.agent import PlannerAgent
from embeddings.embedder import get_embedding_model

def cosine_similarity(vec1, vec2):
    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

def compute_semantic_overlap(gen_queries, exp_queries, embeddings_model):
    """Computes semantic similarity using Sentence Transformer embeddings and Cosine Similarity."""
    if not gen_queries or not exp_queries:
        return 0.0
        
    gen_vecs = embeddings_model.embed_documents(gen_queries)
    exp_vecs = embeddings_model.embed_documents(exp_queries)
    
    # For each expected query, find the highest cosine similarity among generated queries
    max_sims = []
    for e_vec in exp_vecs:
        sims = [cosine_similarity(e_vec, g_vec) for g_vec in gen_vecs]
        max_sims.append(max(sims))
        
    # Average the maximum similarities to ensure all expected aspects were covered
    return sum(max_sims) / len(max_sims)

def evaluate_planner():
    base_dir = os.path.dirname(__file__)
    q_path = os.path.join(base_dir, "dataset", "questions.json")
    exp_path = os.path.join(base_dir, "dataset", "expected_planner.json")
    
    with open(q_path, "r") as f:
        questions = {item["id"]: item["question"] for item in json.load(f)}
        
    with open(exp_path, "r") as f:
        expected = json.load(f)
        
    print("Initializing Planner Agent and Embedding Model for evaluation...")
    planner = PlannerAgent()
    embeddings_model = get_embedding_model()
    
    total = len(expected)
    intent_hits = 0
    decomp_scores = []
    times = []
    
    print(f"\nRunning evaluation on {total} test cases...")
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
            
        # Decomposition Accuracy (Semantic)
        gen_queries = result.get("sub_queries", [])
        exp_queries = exp["sub_queries"]
        score = compute_semantic_overlap(gen_queries, exp_queries, embeddings_model)
        
        decomp_scores.append(score)
        
    avg_intent = (intent_hits / total) * 100
    avg_decomp = (sum(decomp_scores) / total) * 100
    avg_time = sum(times) / total
    
    print("\n=== Planner Agent Metrics ===")
    print(f"Planner Intent Accuracy: {avg_intent:.1f}%")
    print(f"Query Decomposition Accuracy: {avg_decomp:.1f}%")
    print(f"Average Planning Time: {avg_time:.0f} ms")
    
if __name__ == "__main__":
    evaluate_planner()
