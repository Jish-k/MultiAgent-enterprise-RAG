import os
import sys
import json
import time
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.planner.agent import PlannerAgent
from agents.retriever.agent import EvidenceRetrievalAgent
from agents.reasoner.agent import ReasonerAgent
from agents.verifier.agent import VerifierAgent
from llm.provider import get_llm
from langchain_core.messages import SystemMessage, HumanMessage

def count_tokens(text):
    return len(text) // 4  # Approximation

def evaluate_llm_judge(llm, answer, expected_answer):
    if not expected_answer or not answer:
        return 0.0
    prompt = f"Expected Answer: {expected_answer}\nActual Answer: {answer}\nScore the actual answer on a scale from 0.0 to 1.0 based on its completeness and helpfulness compared to the expected answer. Output ONLY the numerical score."
    try:
        res = llm.invoke([SystemMessage(content="You are a strict numeric evaluator."), HumanMessage(content=prompt)]).content.strip()
        import re
        match = re.search(r"0\.\d+|1\.0", res)
        return float(match.group(0)) if match else 0.0
    except:
        return 0.0

def compute_semantic_similarity(ans, exp):
    if not ans or not exp: return 0.0
    try:
        vectorizer = TfidfVectorizer().fit_transform([ans, exp])
        vectors = vectorizer.toarray()
        return float(cosine_similarity([vectors[0]], [vectors[1]])[0][0])
    except:
        return 0.0

def run_benchmark():
    dataset_path = "evaluation/dataset/pilot_questions.json"
    gt_path = "evaluation/dataset/ground_truth.json"
    meta_path = "evaluation/dataset/metadata.json"
    results_dir = "evaluation/results/pilot"
    errors_dir = os.path.join("evaluation/results/errors")
    
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(errors_dir, exist_ok=True)
    
    # Save experiment config
    experiment_config = {
        "experiment_id": "pilot_v1.0",
        "dataset_version": "1.0",
        "pipeline_version": "1.0",
        "benchmark_date": time.strftime("%Y-%m-%d"),
        "llm_provider": "Groq",
        "model": "llama-3.1-8b",
        "temperature": 0.0,
        "embedding_model": "all-MiniLM-L6-v2",
        "vector_database": "ChromaDB",
        "retrieval_top_k": 5,
        "chunk_size": 500,
        "chunk_overlap": 50,
        "runs_per_configuration": 3
    }
    with open(os.path.join(results_dir, "experiment_config.json"), "w") as f:
        json.dump(experiment_config, f, indent=2)
    
    with open(dataset_path, "r") as f: questions = json.load(f)
    with open(gt_path, "r") as f: gt_data = {q["id"]: q for q in json.load(f)}
    with open(meta_path, "r") as f: meta_data = {q["id"]: q for q in json.load(f)}
        
    print(f"Initializing Agents...")
    planner = PlannerAgent()
    retriever = EvidenceRetrievalAgent()
    reasoner = ReasonerAgent()
    verifier = VerifierAgent(threshold=0.50)
    llm = get_llm()
    
    configs = ["A", "B", "C", "D"]
    runs_per_config = 3
    
    all_results = []
    evaluation_breakdown = []
    
    for config in configs:
        print(f"\n=======================")
        print(f"RUNNING CONFIGURATION {config}")
        print(f"=======================")
        
        config_dir = os.path.join(results_dir, f"config_{config}")
        os.makedirs(config_dir, exist_ok=True)
        
        config_results = []
        raw_outputs = []
        
        for run_idx in range(runs_per_config):
            print(f"\n--- Run {run_idx+1}/{runs_per_config} ---")
            
            for i, q in enumerate(questions):
                q_id = q["id"]
                q_text = q.get("question", "")
                expected_ans = gt_data.get(q_id, {}).get("expected_answer", "")
                
                print(f"[{i+1}/{len(questions)}] Processing: {q_id}")
                
                start_time = time.time()
                
                metrics = {
                    "id": q_id,
                    "run": run_idx + 1,
                    "config": config,
                    "retrieval_difficulty": meta_data.get(q_id, {}).get("retrieval_difficulty", "Unknown"),
                    "reasoning_difficulty": meta_data.get(q_id, {}).get("difficulty", "Unknown"),
                    "planner_latency_ms": 0,
                    "retriever_latency_ms": 0,
                    "reasoner_latency_ms": 0,
                    "verifier_latency_ms": 0,
                    "generation_latency_ms": 0,
                    "retriever_input_tokens": 0,
                    "after_dedup_tokens": 0,
                    "after_reasoner_tokens": 0,
                    "generator_input_tokens": 0,
                    "confidence": None,
                    "claim_support_rate": None,
                    "citation_accuracy": None,
                    "ess": None,
                    "accuracy": 0.0,
                    "hallucination_resistance": 0.0,
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0
                }
                
                raw_out = {
                    "id": q_id,
                    "run": run_idx + 1,
                    "config": config,
                    "question": q_text,
                    "answer": "",
                    "retrieved_chunks": []
                }
                
                failure_reason = None
                
                try:
                    plan = {"sub_queries": [q_text], "required_information": []}
                    if config in ["B", "C", "D"]:
                        t0 = time.time()
                        plan = planner.plan(q_text)
                        metrics["planner_latency_ms"] = (time.time() - t0) * 1000
                    
                    t0 = time.time()
                    evidence_pkg = retriever.retrieve(request_id=q_id, sub_queries=plan.get("sub_queries", [q_text]))
                    metrics["retriever_latency_ms"] = (time.time() - t0) * 1000
                    
                    raw_out["retrieved_chunks"] = [c.content for c in evidence_pkg.chunks]
                    metrics["retriever_input_tokens"] = count_tokens(" ".join([c.content for c in evidence_pkg.chunks])) 
                    metrics["after_dedup_tokens"] = metrics["retriever_input_tokens"] 
                    
                    answer = ""
                    used_chunks = evidence_pkg.chunks
                    citation_accuracy = 0.0
                    
                    if config in ["B", "C"]:
                        t0 = time.time()
                        reasoning_out = reasoner.reason(question=q_text, evidence_package=evidence_pkg)
                        metrics["reasoner_latency_ms"] = (time.time() - t0) * 1000
                        
                        answer = reasoning_out.answer
                        used_ids = set(reasoning_out.analysis.used_chunks)
                        used_chunks = [c for c in evidence_pkg.chunks if c.chunk_id in used_ids]
                        
                        metrics["after_reasoner_tokens"] = count_tokens(" ".join([c.content for c in used_chunks]))
                        metrics["generator_input_tokens"] = count_tokens(" ".join(reasoning_out.analysis.key_facts) + " " + " ".join([c.content for c in used_chunks]))
                        
                        if len(used_chunks) > 0:
                            citation_accuracy = len(reasoning_out.analysis.used_chunks) / len(evidence_pkg.chunks) if len(evidence_pkg.chunks) > 0 else 0
                        
                        # Note: actual token usage not tracked by Reasoner, fallback to approximations
                        metrics["prompt_tokens"] = metrics["generator_input_tokens"]
                        metrics["completion_tokens"] = count_tokens(answer)
                        metrics["total_tokens"] = metrics["prompt_tokens"] + metrics["completion_tokens"]
                    else:
                        t0 = time.time()
                        context = "\n".join([c.content for c in evidence_pkg.chunks])
                        if len(context) > 15000: context = context[:15000]
                        
                        metrics["after_reasoner_tokens"] = count_tokens(context)
                        metrics["generator_input_tokens"] = count_tokens(context)
                        
                        prompt = f"Answer the question based ONLY on the context.\nContext: {context}\nQuestion: {q_text}\nAnswer:"
                        res = llm.invoke([SystemMessage(content="You are a precise assistant."), HumanMessage(content=prompt)])
                        answer = res.content.strip()
                        metrics["generation_latency_ms"] = (time.time() - t0) * 1000
                        
                        if hasattr(res, "response_metadata") and "token_usage" in res.response_metadata:
                            t_usage = res.response_metadata["token_usage"]
                            metrics["prompt_tokens"] = t_usage.get("prompt_tokens", 0)
                            metrics["completion_tokens"] = t_usage.get("completion_tokens", 0)
                            metrics["total_tokens"] = t_usage.get("total_tokens", 0)

                    raw_out["answer"] = answer

                    ess = 0.0
                    claim_support = 0.0
                    citation_acc = citation_accuracy
                    if config == "C":
                        t0 = time.time()
                        verifier_resp = verifier.verify(draft_answer=answer, used_chunks=used_chunks, required_information=plan.get("required_information", []))
                        metrics["verifier_latency_ms"] = (time.time() - t0) * 1000
                        
                        v_metrics = verifier_resp.verification_metrics
                        metrics["confidence"] = v_metrics.average_confidence
                        metrics["ess"] = v_metrics.evidence_sufficiency_score
                        metrics["claim_support_rate"] = v_metrics.claim_support_rate
                        metrics["citation_accuracy"] = v_metrics.citation_accuracy
                        
                        raw_out["confidence"] = v_metrics.average_confidence
                        ess = metrics["ess"]
                        claim_support = metrics["claim_support_rate"]
                        citation_acc = metrics["citation_accuracy"]
                        
                        metrics["hallucination_resistance"] = (
                            v_metrics.claim_support_rate * v_metrics.average_confidence
                        )
                        
                    metrics["e2e_latency_ms"] = (time.time() - start_time) * 1000
                    
                    exact_match = 1.0 if expected_ans.lower() in answer.lower() else 0.0
                    semantic_sim = compute_semantic_similarity(answer, expected_ans)
                    llm_judge = evaluate_llm_judge(llm, answer, expected_ans)
                    
                    rule_based = (0.5 * semantic_sim) + (0.5 * exact_match)
                    final_score = (0.40 * rule_based) + (0.60 * llm_judge)
                    metrics["accuracy"] = final_score
                    
                    evaluation_breakdown.append({
                        "QID": q_id,
                        "Config": config,
                        "Run": run_idx + 1,
                        "Exact": exact_match,
                        "Semantic": semantic_sim,
                        "Citation": citation_accuracy,
                        "ESS": ess,
                        "Claim Support Rate": claim_support,
                        "Citation Accuracy": citation_acc,
                        "LLM Judge": llm_judge,
                        "Confidence": 0.0 if metrics.get("confidence") is None else metrics.get("confidence"),
                        "Final": final_score
                    })
                    
                    if final_score < 0.5:
                        failure_reason = f"Low Final Accuracy Score: {final_score:.2f}"
                    
                except Exception as e:
                    print(f"Error on {q_id}: {e}")
                    failure_reason = f"Exception: {str(e)}\n{traceback.format_exc()}"
                    raw_out["answer"] = f"ERROR: {e}"

                config_results.append(metrics)
                raw_outputs.append(raw_out)
                all_results.append(metrics)
                
                # Log error file if failed
                if failure_reason:
                    err_payload = {
                        "Question": q_text,
                        "Config": config,
                        "Run": run_idx + 1,
                        "Expected Answer": expected_ans,
                        "Generated Answer": raw_out["answer"],
                        "Retrieved Chunks": raw_out["retrieved_chunks"],
                        "Planner Output": plan if config in ["B", "C", "D"] else "N/A",
                        "Confidence": metrics["confidence"],
                        "ESS": metrics["ess"],
                        "Final Score": metrics.get("accuracy", 0.0),
                        "Failure Reason": failure_reason
                    }
                    with open(os.path.join(errors_dir, f"{config}_run{run_idx+1}_{q_id}.json"), "w") as f:
                        json.dump(err_payload, f, indent=2)
                        
                time.sleep(1)
                
        with open(os.path.join(config_dir, "raw_outputs.json"), "w") as f: json.dump(raw_outputs, f, indent=2)
        with open(os.path.join(config_dir, "metrics.json"), "w") as f: json.dump(config_results, f, indent=2)
            
    df = pd.DataFrame(all_results)
    df.to_csv(os.path.join(results_dir, "pilot_benchmark_data.csv"), index=False)
    
    breakdown_df = pd.DataFrame(evaluation_breakdown)
    breakdown_df.to_csv(os.path.join(results_dir, "evaluation_breakdown.csv"), index=False)
    
    print("\nBenchmark completed. Results saved.")

if __name__ == "__main__":
    run_benchmark()
