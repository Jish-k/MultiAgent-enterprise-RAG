import os
import sys
import glob

# Add the project root to sys.path to allow absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Config
from ingestion.hotpot_loader import load_hotpotqa
from ingestion.cleaner import clean_pages
from ingestion.metadata import extract_metadata
from ingestion.chunker import chunk_documents
from embeddings.vector_store import add_to_vector_store

def run_hotpotqa_ingestion():
    print("Running HotpotQA Ingestion Pipeline...")
    
    # 1. Load
    pages = load_hotpotqa(subset_size=Config.HOTPOTQA_SUBSET_SIZE)
    
    # 2. Clean (HotpotQA text might not need aggressive cleaning, but it's safe to run it through)
    pages = clean_pages(pages)
    
    # 3. Metadata (Section extraction won't do much for HotpotQA, but let's keep consistency)
    pages = extract_metadata(pages)
    
    # 4. Chunk
    chunks = chunk_documents(pages)
    print(f"  -> Extracted {len(chunks)} chunks from HotpotQA.")
    
    # 5. Embed and Store
    if chunks:
        print("\n--- Starting Vector Embedding Phase ---")
        add_to_vector_store(chunks)
        
    return chunks

def run_ingestion_pipeline():
    return run_hotpotqa_ingestion()

if __name__ == "__main__":
    run_ingestion_pipeline()
