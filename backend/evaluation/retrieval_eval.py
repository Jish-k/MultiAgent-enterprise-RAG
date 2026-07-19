import json
import time
import os
import sys
import numpy as np
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.planner.agent import PlannerAgent
from agents.retriever.agent import EvidenceRetrievalAgent
from evaluation.plots import generate_stage3_plots

def compute_ndcg(retrieved_docs, expected_docs, k=5):
    """Computes Normalized Discounted Cumulative Gain (nDCG@k)."""
    dcg = 0.0
    idcg = 0.0
    
    # Calculate DCG
    for i, doc in enumerate(retrieved_docs[:k]):
        rel = 1.0 if doc in expected_docs else 0.0
        dcg += rel / math.log2(i + 2) # i+2 because rank is 1-indexed (i=0 -> log2(2)=1)
        
    # Calculate IDCG (Ideal DCG where all expected docs are at the top)
    for i in range(min(k, len(expected_docs))):
        idcg += 1.0 / math.log2(i + 2)
        
    if idcg == 0:
        return 0.0
    return dcg / idcg

def evaluate_retriever():
    base_dir = os.path.dirname(__file__)
    
    with open(os.path.join(base_dir, "dataset", "questions.json"), "r") as f:
        questions = {item["id"]: item["question"] for item in json.load(f)}
        
    with open(os.path.join(base_dir, "dataset", "metadata.json"), "r") as f:
        metadata = {item["id"]: item["documents"] for item in json.load(f)}
        
    print("Initializing Agents...")
    planner = PlannerAgent()
    retriever = EvidenceRetrievalAgent()
    
    metrics = {
        "recall_1": 0,
        "recall_3": 0,
        "recall_5": 0,
        "mrr": 0.0,
        "ndcg_5": 0.0,
        "planner_time": [],
        "search_time": [],
        "merge_time": [],
        "dedup_time": [],
        "rank_time": [],
        "chunks_retrieved": [],
        "duplicates_removed": [],
        "chunks_retained": []
    }
    
    total = len(questions)
    
    for qid, q_text in questions.items():
        expected_docs = metadata.get(qid, [])
        if not expected_docs:
            continue
            
        # 1. Planner
        start_plan = time.time()
        plan = planner.plan(q_text)
        sub_queries = plan.get("sub_queries", [q_text])
        metrics["planner_time"].append((time.time() - start_plan) * 1000)
        
        # 2. Retriever
        package = retriever.retrieve(request_id=str(qid), sub_queries=sub_queries)
        
        # Track Latency & Efficiency
        rm = package.retrieval_metrics
        metrics["search_time"].append(rm.search_time_ms)
        metrics["merge_time"].append(rm.merge_time_ms)
        metrics["dedup_time"].append(rm.dedup_time_ms)
        metrics["rank_time"].append(rm.ranking_time_ms)
        
        metrics["chunks_retrieved"].append(rm.chunks_retrieved_total)
        metrics["duplicates_removed"].append(rm.duplicates_removed)
        metrics["chunks_retained"].append(rm.chunks_after_dedup)
        
        # Get retrieved document list
        retrieved_docs = [chunk.document for chunk in package.chunks]
        
        # Recall@k
        if any(doc in expected_docs for doc in retrieved_docs[:1]): metrics["recall_1"] += 1
        if any(doc in expected_docs for doc in retrieved_docs[:3]): metrics["recall_3"] += 1
        if any(doc in expected_docs for doc in retrieved_docs[:5]): metrics["recall_5"] += 1
        
        # MRR
        for rank, doc in enumerate(retrieved_docs):
            if doc in expected_docs:
                metrics["mrr"] += 1.0 / (rank + 1)
                break
                
        # nDCG@5
        metrics["ndcg_5"] += compute_ndcg(retrieved_docs, expected_docs, k=5)
        
    # Aggregate
    print("\n=== Retrieval Quality ===")
    print(f"Recall@1: {(metrics['recall_1']/total)*100:.1f}%")
    print(f"Recall@3: {(metrics['recall_3']/total)*100:.1f}%")
    print(f"Recall@5: {(metrics['recall_5']/total)*100:.1f}%")
    print(f"MRR:      {metrics['mrr']/total:.3f}")
    print(f"nDCG@5:   {metrics['ndcg_5']/total:.3f}")
    
    print("\n=== Evidence Quality ===")
    total_retrieved = sum(metrics['chunks_retrieved'])
    total_removed = sum(metrics['duplicates_removed'])
    dedup_rate = (total_removed / total_retrieved * 100) if total_retrieved > 0 else 0
    print(f"Total Chunks Retrieved: {total_retrieved}")
    print(f"Duplicates Removed:     {total_removed}")
    print(f"Duplicate Removal Rate: {dedup_rate:.1f}%")
    print(f"Avg Evidence Size:      {np.mean(metrics['chunks_retained']):.1f} chunks")
    
    print("\n=== Latency Breakdown ===")
    print(f"Planner:       {np.mean(metrics['planner_time']):.0f} ms")
    print(f"Search:        {np.mean(metrics['search_time']):.0f} ms")
    print(f"Merge:         {np.mean(metrics['merge_time']):.0f} ms")
    print(f"Deduplication: {np.mean(metrics['dedup_time']):.0f} ms")
    print(f"Ranking:       {np.mean(metrics['rank_time']):.0f} ms")
    
    print("\nGenerating Plots...")
    recall_vals = [
        (metrics['recall_1']/total)*100,
        (metrics['recall_3']/total)*100,
        (metrics['recall_5']/total)*100
    ]
    latencies = [
        np.mean(metrics['planner_time']),
        np.mean(metrics['search_time']),
        np.mean(metrics['merge_time']),
        np.mean(metrics['dedup_time']),
        np.mean(metrics['rank_time'])
    ]
    dedup_sizes = [
        (total_retrieved - total_removed) / total_retrieved * 100 if total_retrieved > 0 else 50,
        dedup_rate
    ]
    
    generate_stage3_plots(recall_vals, latencies, dedup_sizes)

if __name__ == "__main__":
    evaluate_retriever()
