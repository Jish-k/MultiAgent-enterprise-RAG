import os
import sys
import glob

# Add the project root to sys.path to allow absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ingestion.loader import load_pdf
from ingestion.cleaner import clean_pages
from ingestion.metadata import extract_metadata
from ingestion.chunker import chunk_documents
from embeddings.vector_store import add_to_vector_store

def run_ingestion_pipeline(raw_docs_dir="data/raw_documents"):
    pdf_files = glob.glob(os.path.join(raw_docs_dir, "*.pdf"))
    if not pdf_files:
        # Fallback if run from project root instead of ingestion folder
        pdf_files = glob.glob(os.path.join("data/raw_documents", "*.pdf"))
        
    print(f"Found {len(pdf_files)} PDF files to ingest.")
    
    all_chunks = []
    
    for pdf_file in pdf_files:
        print(f"\nProcessing: {os.path.basename(pdf_file)}")
        
        # 1. Load
        pages = load_pdf(pdf_file)
        
        # 2. Clean
        pages = clean_pages(pages)
        
        # 3. Metadata
        pages = extract_metadata(pages)
        
        # 4. Chunk
        chunks = chunk_documents(pages)
        print(f"  -> Extracted {len(chunks)} chunks.")
        
        all_chunks.extend(chunks)
        
    print(f"\nTotal chunks generated across all documents: {len(all_chunks)}")
    
    # 5. Embed and Store
    if all_chunks:
        print("\n--- Starting Vector Embedding Phase ---")
        add_to_vector_store(all_chunks)
        
    return all_chunks

if __name__ == "__main__":
    run_ingestion_pipeline()
