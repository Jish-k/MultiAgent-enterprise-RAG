import os
import glob
from loader import load_pdf
from cleaner import clean_pages
from metadata import extract_metadata
from chunker import chunk_documents

def run_ingestion_pipeline(raw_docs_dir="../data/raw_documents"):
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
        print(f"  -> Loaded {len(pages)} pages.")
        
        # 2. Clean
        pages = clean_pages(pages)
        print("  -> Cleaned text.")
        
        # 3. Metadata
        pages = extract_metadata(pages)
        print("  -> Extracted metadata.")
        
        # 4. Chunk
        chunks = chunk_documents(pages)
        print(f"  -> Created {len(chunks)} chunks.")
        
        all_chunks.extend(chunks)
        
    print(f"\nTotal chunks generated across all documents: {len(all_chunks)}")
    return all_chunks

if __name__ == "__main__":
    run_ingestion_pipeline()
