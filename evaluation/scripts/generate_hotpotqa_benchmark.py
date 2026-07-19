import os
import json
import random
from datasets import load_dataset

def generate_benchmark():
    # Define buckets
    target_counts = {
        "bridge": {"easy": 20, "medium": 20, "hard": 20},
        "comparison": {"easy": 20, "medium": 20, "hard": 20}
    }
    
    current_counts = {
        "bridge": {"easy": 0, "medium": 0, "hard": 0},
        "comparison": {"easy": 0, "medium": 0, "hard": 0}
    }
    
    benchmark_data = []
    
    print("Loading HotpotQA train split...")
    dataset = list(load_dataset('hotpotqa/hotpot_qa', 'fullwiki', split='train'))
    
    # Shuffle to ensure random sample
    random.seed(42)
    random.shuffle(dataset)
    
    print("Filtering and balancing dataset...")
    for item in dataset:
        rtype = item.get("type")
        level = item.get("level")
        
        if rtype in target_counts and level in target_counts[rtype]:
            if current_counts[rtype][level] < target_counts[rtype][level]:
                
                # Transform to required schema
                benchmark_entry = {
                    "id": item["id"],
                    "question": item["question"],
                    "answer": item["answer"],
                    "difficulty": level,
                    "reasoning_type": rtype,
                    "supporting_titles": item["supporting_facts"]["title"],
                    "supporting_sentence_ids": item["supporting_facts"]["sent_id"]
                }
                
                benchmark_data.append(benchmark_entry)
                current_counts[rtype][level] += 1
                
                # Check if we are done
                all_done = True
                for r in target_counts:
                    for l in target_counts[r]:
                        if current_counts[r][l] < target_counts[r][l]:
                            all_done = False
                            break
                
                if all_done:
                    break
                    
    # Save to file
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "hotpotqa_benchmark_v1.json")
    
    with open(out_file, "w") as f:
        json.dump(benchmark_data, f, indent=2)
        
    print(f"Generated benchmark with {len(benchmark_data)} questions.")
    print("Distribution:")
    for rtype, levels in current_counts.items():
        for level, count in levels.items():
            print(f"  {rtype.capitalize()} - {level.capitalize()}: {count}")
    print(f"\nSaved to: {out_file}")

if __name__ == "__main__":
    generate_benchmark()
