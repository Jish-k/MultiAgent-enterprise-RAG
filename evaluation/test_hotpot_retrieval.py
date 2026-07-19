import os
import sys
import random

# Force the config to use hotpotqa dataset collection
os.environ["DATASET_SOURCE"] = "hotpotqa"

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datasets import load_dataset
from embeddings.retrieval import get_retriever
from config import Config

def evaluate_hotpot_retrieval(num_questions=30, top_k=5):
    print(f"Loading HotpotQA subset (size={Config.HOTPOTQA_SUBSET_SIZE}) for evaluation...")
    dataset = load_dataset('hotpotqa/hotpot_qa', 'fullwiki', split='validation')
    subset = dataset.select(range(min(Config.HOTPOTQA_SUBSET_SIZE, len(dataset))))
    
    # Pick random questions
    test_indices = random.sample(range(len(subset)), min(num_questions, len(subset)))
    test_samples = [subset[i] for i in test_indices]
    
    print(f"\nInitializing Retriever (k={top_k}) for collection: {Config.ACTIVE_CHROMA_COLLECTION}...")
    retriever = get_retriever(k=top_k)
    
    total_queries = len(test_samples)
    at_least_one_hit = 0
    all_hits = 0
    
    print(f"Running {total_queries} test queries...\n")
    print("-" * 80)
    
    hits_at_1 = 0
    hits_at_3 = 0
    hits_at_5 = 0
    mrr_sum = 0.0
    
    for i, sample in enumerate(test_samples, 1):
        question = sample['question']
        # The expected documents are the unique titles in supporting_facts
        expected_titles = set(sample['supporting_facts']['title'])
        
        # Retrieve documents
        docs = retriever.invoke(question)
        
        # Calculate rank of first hit
        first_hit_rank = None
        retrieved_sources = []
        for rank, doc in enumerate(docs, 1):
            source = doc.metadata.get("source")
            if source:
                retrieved_sources.append(source)
                if source in expected_titles and first_hit_rank is None:
                    first_hit_rank = rank
                    
        # Update metrics
        if first_hit_rank is not None:
            if first_hit_rank <= 1:
                hits_at_1 += 1
            if first_hit_rank <= 3:
                hits_at_3 += 1
            if first_hit_rank <= 5:
                hits_at_5 += 1
            mrr_sum += 1.0 / first_hit_rank
            
        print(f"Q{i}: {question}")
        print(f"  Expected: {list(expected_titles)}")
        print(f"  Retrieved: {retrieved_sources}")
        
        if first_hit_rank is not None:
            print(f"  Result: ✅ HIT at Rank {first_hit_rank}")
        else:
            print("  Result: ❌ MISS (No supporting docs found in Top-5)")
        print("-" * 80)
        
    mrr = mrr_sum / total_queries if total_queries > 0 else 0.0
    
    print("\n" + "=" * 40)
    print("🎯 HOTPOTQA RETRIEVAL EVALUATION RESULTS")
    print("=" * 40)
    print(f"Total Questions Evaluated: {total_queries}")
    print(f"Recall@1: {hits_at_1}/{total_queries} ({(hits_at_1/total_queries)*100:.1f}%)")
    print(f"Recall@3: {hits_at_3}/{total_queries} ({(hits_at_3/total_queries)*100:.1f}%)")
    print(f"Recall@5: {hits_at_5}/{total_queries} ({(hits_at_5/total_queries)*100:.1f}%)")
    print(f"Mean Reciprocal Rank (MRR): {mrr:.4f}")
    print("=" * 40)

if __name__ == "__main__":
    evaluate_hotpot_retrieval(num_questions=30, top_k=5)
