import os
import sys
import json
import time
import csv
import re
import string

os.environ["DATASET_SOURCE"] = "hotpotqa"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from langchain_community.callbacks import get_openai_callback
from langchain_core.output_parsers import StrOutputParser

from llm.provider import get_llm
from rag.retriever import format_docs
from agent.planner import get_planner_retriever
from agent.reasoner import build_reasoner_chain, build_reasoner_generator_prompt

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
    results_csv_path = os.path.join(os.path.dirname(__file__), "../agentic_stage2_results.csv")
    report_md_path = os.path.join(os.path.dirname(__file__), "../agentic_stage2_report.md")
    
    with open(benchmark_path, "r") as f:
        dataset = json.load(f)
        
    print(f"Loaded {len(dataset)} questions from benchmark.")
    
    planner_retriever = get_planner_retriever()
    reasoner_chain = build_reasoner_chain()
    
    llm = get_llm()
    gen_prompt = build_reasoner_generator_prompt()
    generator_chain = gen_prompt | llm | StrOutputParser()
    
    results = []
    total_acc = 0
    total_latency = 0
    total_recall = 0
    total_mrr = 0.0
    total_input_tokens = 0
    total_output_tokens = 0
    
    for i, item in enumerate(dataset, 1):
        question = item["question"]
        expected_answer = item["answer"]
        expected_titles = set(item["supporting_titles"])
        
        print(f"[{i}/{len(dataset)}] Q: {question}")
        
        start_time = time.time()
        with get_openai_callback() as cb:
            # 1. Retrieve using Planner
            retrieved_docs = planner_retriever.invoke(question)
            
            # Calculate recall metrics
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
            
            context_str = format_docs(retrieved_docs)
            
            # 2. Reasoner Step
            reasoning_trace = reasoner_chain.invoke({"context": context_str, "question": question})
            
            # 3. Final Generator Step
            prediction = generator_chain.invoke({
                "context": context_str,
                "reasoning": reasoning_trace,
                "question": question
            })
            
        latency = time.time() - start_time
        
        norm_gt = normalize_answer(expected_answer)
        norm_pred = normalize_answer(prediction)
        is_correct = 1 if norm_gt in norm_pred else 0
        
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
            "prediction": prediction.replace('\n', ' '),
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
        
    n = len(dataset)
    md_content = f"""# Agentic RAG Stage 2 Evaluation Report
## Architecture: Planner -> Retriever -> Reasoner -> LLM

## Aggregate Metrics
- **Total Questions:** {n}
- **Accuracy (Substring Match):** {(total_acc/n)*100:.2f}%
- **Average Latency:** {total_latency/n:.2f} seconds
- **Retrieval Recall (Hit@K):** {(total_recall/n)*100:.2f}%
- **Mean Reciprocal Rank (MRR):** {total_mrr/n:.4f}
- **Avg Prompt Tokens:** {total_input_tokens/n:.1f}
- **Avg Completion Tokens:** {total_output_tokens/n:.1f}
"""
    with open(report_md_path, "w") as f:
        f.write(md_content)
        
    print(f"\nDone! Results saved to:\n- {results_csv_path}\n- {report_md_path}")

if __name__ == "__main__":
    main()
