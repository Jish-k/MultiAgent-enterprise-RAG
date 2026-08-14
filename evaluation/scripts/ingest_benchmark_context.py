import os
import sys
import json

# Ensure dataset uses hotpotqa collection
os.environ["DATASET_SOURCE"] = "hotpotqa"

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from datasets import load_dataset
from embeddings.vector_store import add_to_vector_store, get_vector_store
from ingestion.cleaner import clean_pages
from ingestion.metadata import extract_metadata
from ingestion.chunker import chunk_documents

def ingest_benchmark_context():
    benchmark_path = os.path.join(os.path.dirname(__file__), "../datasets/hotpotqa_benchmark_v1.json")
    with open(benchmark_path, "r") as f:
        benchmark_data = json.load(f)
        
    # Get set of all question IDs in the benchmark
    benchmark_ids = set(item["id"] for item in benchmark_data)
    print(f"Loaded {len(benchmark_ids)} unique question IDs from benchmark.")
    
    print("Loading HotpotQA train split...")
    dataset = load_dataset('hotpotqa/hotpot_qa', 'fullwiki', split='train')
    
    print("Finding matching questions and extracting context...")
    pages_data = []
    seen_titles = set()
    
    # Filter dataset for the benchmark questions
    filtered_dataset = dataset.filter(lambda x: x["id"] in benchmark_ids)
    print(f"Found {len(filtered_dataset)} matching questions in train split.")
    
    for item in filtered_dataset:
        context = item.get("context", {})
        titles = context.get("title", [])
        sentences_list = context.get("sentences", [])
        
        for title, sentences in zip(titles, sentences_list):
            if title in seen_titles:
                continue
                
            seen_titles.add(title)
            
            # Combine sentences into a single paragraph text
            text = " ".join(sentences)
            
            pages_data.append({
                "page_number": 1,
                "text": text,
                "source": title
            })
            
    print(f"Extracted {len(pages_data)} unique context documents for the benchmark.")
    
    print("\nCleaning documents...")
    pages = clean_pages(pages_data)
    
    print("Extracting metadata...")
    pages = extract_metadata(pages)
    
    print("Chunking documents...")
    chunks = chunk_documents(pages)
    print(f"  -> Extracted {len(chunks)} chunks.")
    
    if chunks:
        # Wipe old collection
        print("\nWiping old 'hotpotqa_docs' collection...")
        try:
            vs = get_vector_store()
            vs._client.delete_collection("hotpotqa_docs")
            get_vector_store.cache_clear()  # Clear cache to force a new Chroma instance
            print("Successfully deleted old collection.")
        except Exception as e:
            print(f"Note on wiping collection: {e}")
            
        print("\n--- Starting Vector Embedding Phase ---")
        add_to_vector_store(chunks)
        print("\nBenchmark context successfully ingested!")
        
if __name__ == "__main__":
    ingest_benchmark_context()
