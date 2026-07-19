import json
import time
import os
import sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.planner.agent import PlannerAgent
from agents.retriever.agent import EvidenceRetrievalAgent
from agents.reasoner.agent import ReasonerAgent

def evaluate_reasoner():
    base_dir = os.path.dirname(__file__)
    
    with open(os.path.join(base_dir, "dataset", "questions.json"), "r") as f:
        questions = {item["id"]: item["question"] for item in json.load(f)}
        
    print("Initializing Agents...")
    planner = PlannerAgent()
    retriever = EvidenceRetrievalAgent()
    reasoner = ReasonerAgent()
    
    metrics = {
        "planner_latency": [],
        "retriever_latency": [],
        "analysis_latency": [],
        "generation_latency": [],
        "total_latency": [],
        "evidence_utilization_rates": [],
        "draft_lengths": [],
        "conflict_detection": 0
    }
    
    total = len(questions)
    
    print(f"\nEvaluating Stage 4 Reasoner Pipeline on {total} questions...\n")
    
    for qid, q_text in questions.items():
        total_start = time.time()
        
        # 1. Planner
        start = time.time()
        plan = planner.plan(q_text)
        sub_queries = plan.get("sub_queries", [q_text])
        metrics["planner_latency"].append((time.time() - start) * 1000)
        
        # 2. Retriever
        start = time.time()
        evidence_package = retriever.retrieve(request_id=str(qid), sub_queries=sub_queries)
        metrics["retriever_latency"].append((time.time() - start) * 1000)
        
        # 3. Reasoner
        start = time.time()
        output = reasoner.reason(q_text, evidence_package)
        metrics["analysis_latency"].append(output.metrics.analysis_time_ms)
        metrics["generation_latency"].append(output.metrics.generation_time_ms)
        
        # Metrics Collection
        metrics["evidence_utilization_rates"].append(output.metrics.evidence_utilization_rate)
        metrics["draft_lengths"].append(len(output.answer.split()))
        metrics["total_latency"].append((time.time() - total_start) * 1000)
        
        if len(output.analysis.conflicts) > 0:
            metrics["conflict_detection"] += 1
            
        print(f"[{qid}] Utilization: {output.metrics.evidence_utilization_rate:.1f}% | Latency: {(time.time() - total_start):.2f}s")
        
    print("\n=== Stage 4: Reasoner Evaluation ===")
    print(f"Average Evidence Utilization Rate: {np.mean(metrics['evidence_utilization_rates']):.1f}%")
    print(f"Average Draft Length (words):      {np.mean(metrics['draft_lengths']):.1f}")
    print(f"Total Conflicts Detected:          {metrics['conflict_detection']}")
    
    print("\n=== End-to-End Latency Breakdown ===")
    print(f"Planner Agent:   {np.mean(metrics['planner_latency']):.0f} ms")
    print(f"Retriever Agent: {np.mean(metrics['retriever_latency']):.0f} ms")
    print(f"Reasoner (Anal): {np.mean(metrics['analysis_latency']):.0f} ms")
    print(f"Reasoner (Gen):  {np.mean(metrics['generation_latency']):.0f} ms")
    print(f"-----------------------------------")
    print(f"Total E2E:       {np.mean(metrics['total_latency']):.0f} ms")

if __name__ == "__main__":
    evaluate_reasoner()
