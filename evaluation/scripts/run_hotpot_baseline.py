import os
import sys
import json
import time
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
import openai
import csv
import re
import string

# Ensure dataset uses hotpotqa collection
os.environ["DATASET_SOURCE"] = "hotpotqa"

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from langchain_community.callbacks import get_openai_callback
from rag.generator import build_rag_chain
from rag.retriever import get_rag_retriever

def normalize_answer(s):
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)
    def white_space_fix(text):
        return ' '.join(text.split())
    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)
    return white_space_fix(remove_articles(remove_punc(s.lower())))

def main():
    benchmark_path = os.path.join(os.path.dirname(__file__), "../datasets/hotpotqa_benchmark_v1.json")
    results_csv_path = os.path.join(os.path.dirname(__file__), "../hotpot_baseline_results.csv")
    report_md_path = os.path.join(os.path.dirname(__file__), "../baseline_rag_report.md")
    json_results_path = os.path.join(os.path.dirname(__file__), "../../results/baseline.json")
    
    with open(benchmark_path, "r") as f:
        dataset = json.load(f)
        
    print(f"Loaded {len(dataset)} questions from benchmark.")
    
    rag_chain = build_rag_chain()
    retriever = get_rag_retriever()
    
    results = []
    
    total_acc = 0
    total_latency = 0
    total_recall = 0  # At least one doc found
    total_mrr = 0.0
    total_input_tokens = 0
    total_output_tokens = 0
    
    for i, item in enumerate(dataset, 1):
        question = item["question"]
        expected_answer = item["answer"]
        expected_titles = set(item["supporting_titles"])
        
        print(f"[{i}/{len(dataset)}] Q: {question}")
        
        # 1. Retrieve explicitly to calculate retrieval metrics
        retrieved_docs = retriever.invoke(question)
        retrieved_sources = []
        first_hit_rank = None
        
        for rank, doc in enumerate(retrieved_docs, 1):
            source = doc.metadata.get("source")
            if source:
                retrieved_sources.append(source)
                if source in expected_titles and first_hit_rank is None:
                    first_hit_rank = rank
                    
        mrr = 1.0 / first_hit_rank if first_hit_rank else 0.0
        recall_hit = 1 if first_hit_rank else 0
        citations_str = "|".join(retrieved_sources)
        
        # 2. Run full chain with timing and token tracking
        time.sleep(10)  # Rate limiting
        start_time = time.time()
        with get_openai_callback() as cb:
            prediction = rag_chain.invoke(question)
        latency = time.time() - start_time
        
        # 3. Calculate accuracy
        norm_gt = normalize_answer(expected_answer)
        norm_pred = normalize_answer(prediction)
        is_correct = 1 if norm_gt in norm_pred else 0
        
        # Track metrics
        total_acc += is_correct
        total_latency += latency
        total_recall += recall_hit
        total_mrr += mrr
        total_input_tokens += cb.prompt_tokens
        total_output_tokens += cb.completion_tokens
        
        result_row = {
            "id": item["id"],
            "difficulty": item["difficulty"],
            "reasoning_type": item["reasoning_type"],
            "question": question,
            "expected_answer": expected_answer,
            "prediction": prediction.replace('\n', ' '), # Keep csv clean
            "citations": citations_str,
            "is_correct": is_correct,
            "latency": latency,
            "mrr": mrr,
            "recall_hit": recall_hit,
            "prompt_tokens": cb.prompt_tokens,
            "completion_tokens": cb.completion_tokens
        }
        results.append(result_row)
        print(f"   Correct: {bool(is_correct)} | Latency: {latency:.2f}s | Tokens: {cb.total_tokens}")

    # Write CSV
    with open(results_csv_path, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
        
    # Calculate aggregates
    n = len(dataset)
    agg_acc = total_acc / n
    agg_latency = total_latency / n
    agg_recall = total_recall / n
    agg_mrr = total_mrr / n
    agg_in_tokens = total_input_tokens / n
    agg_out_tokens = total_output_tokens / n
    
    # Write MD Report
    md_content = f"""# HotpotQA Baseline RAG Evaluation Report

## Aggregate Metrics
- **Total Questions:** {n}
- **Accuracy (Substring Match):** {agg_acc*100:.2f}%
- **Average Latency:** {agg_latency:.2f} seconds
- **Retrieval Recall (Hit@K):** {agg_recall*100:.2f}%
- **Mean Reciprocal Rank (MRR):** {agg_mrr:.4f}
- **Avg Prompt Tokens:** {agg_in_tokens:.1f}
- **Avg Completion Tokens:** {agg_out_tokens:.1f}
"""
    with open(report_md_path, "w") as f:
        f.write(md_content)
        
    # Write JSON results for frontend
    os.makedirs(os.path.dirname(json_results_path), exist_ok=True)
    with open(json_results_path, "w") as f:
        json.dump({
            "accuracy": round(agg_acc * 100, 2),
            "recall": round(agg_recall * 100, 2),
            "latency": round(agg_latency, 2),
            "mrr": round(agg_mrr, 4)
        }, f, indent=4)
        
    print(f"\nDone! Results saved to:\n- {results_csv_path}\n- {report_md_path}\n- {json_results_path}")

if __name__ == "__main__":
    main()
