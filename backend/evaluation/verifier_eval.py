import sys
import os
import json
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.planner.agent import PlannerAgent
from agents.retriever.agent import EvidenceRetrievalAgent
from agents.reasoner.agent import ReasonerAgent
from agents.verifier.agent import VerifierAgent

def run_evaluation():
    print("Initializing Agents...")
    planner = PlannerAgent()
    retriever = EvidenceRetrievalAgent()
    reasoner = ReasonerAgent()
    verifier = VerifierAgent(threshold=0.50)
    
    dataset_path = "evaluation/dataset/questions.json"
    with open(dataset_path, "r") as f:
        questions = json.load(f)
        
    total_latency = 0
    total_claims = 0
    total_supported = 0
    total_unsupported = 0
    total_ess = 0.0
    total_confidence = 0.0
    
    print(f"\nEvaluating Stage 5 Verifier Pipeline on {len(questions)} questions...\n")
    
    for i, q in enumerate(questions):
        q_text = q["question"]
        
        start_time = time.time()
        
        # 1. Planner
        plan = planner.plan(q_text)
        req_info = plan.get("required_information", [])
        
        # 2. Retriever
        evidence_pkg = retriever.retrieve("eval_req", plan["sub_queries"])
        
        # 3. Reasoner
        reasoning_output = reasoner.reason(q_text, evidence_pkg)
        draft_answer = reasoning_output.answer
        
        # The Reasoner output returns the chunk_ids of the chunks it actually used.
        used_chunk_ids = set(reasoning_output.analysis.used_chunks)
        used_chunks = [c for c in evidence_pkg.chunks if c.chunk_id in used_chunk_ids]
        
        # 4. Verifier
        verifier_response = verifier.verify(
            draft_answer=draft_answer,
            used_chunks=used_chunks,
            required_information=req_info
        )
        
        latency = (time.time() - start_time) * 1000
        total_latency += latency
        
        metrics = verifier_response.verification_metrics
        total_claims += len(verifier_response.claims)
        total_supported += len(verifier_response.supported_claims)
        total_unsupported += metrics.unsupported_claim_count
        total_ess += metrics.evidence_sufficiency_score
        total_confidence += metrics.average_confidence
        
        print(f"[{i+1}] Conf: {metrics.average_confidence:.2f} | ESS: {metrics.evidence_sufficiency_score:.2f} | Unsupp Claims: {metrics.unsupported_claim_count} | Latency: {latency/1000:.2f}s")
        
    num_qs = len(questions)
    
    print("\n=== Stage 5: Verifier Evaluation ===")
    print(f"Average Confidence:        {total_confidence / num_qs:.2f}")
    print(f"Average ESS:               {total_ess / num_qs:.2f}")
    print(f"Overall Claim Support Rate: {(total_supported / total_claims * 100) if total_claims > 0 else 0:.1f}%")
    print(f"Total Unsupported Claims:  {total_unsupported} (Hallucination Triggers)")
    print(f"Average E2E Latency:       {total_latency / num_qs / 1000:.2f}s")

if __name__ == "__main__":
    run_evaluation()
