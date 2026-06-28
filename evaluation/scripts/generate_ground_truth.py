import json
import os
import time
import pypdf
import sys
from langchain_core.messages import SystemMessage, HumanMessage

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from llm.provider import get_llm

QUESTIONS_PATH = "evaluation/dataset/questions.json"
CHECKPOINT_PATH = "evaluation/dataset/ground_truth.json"
RAW_DOCS_DIR = "data/raw_documents"
BATCH_SIZE = 20

def get_pdf_text(filenames):
    text = ""
    for filename in filenames:
        path = os.path.join(RAW_DOCS_DIR, filename)
        if not os.path.exists(path):
            print(f"Warning: {filename} not found.")
            continue
        try:
            reader = pypdf.PdfReader(path)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading {filename}: {e}")
    return text

def generate_ground_truth():
    with open(QUESTIONS_PATH, "r") as f:
        questions = json.load(f)

    if os.path.exists(CHECKPOINT_PATH):
        with open(CHECKPOINT_PATH, "r") as f:
            ground_truth = json.load(f)
    else:
        ground_truth = []

    processed_ids = {item["id"] for item in ground_truth if "Error generating answer" not in item.get("expected_answer", "")}
    llm = get_llm()
    
    batch_count = 0
    for q in questions:
        if q["id"] in processed_ids:
            continue
            
        print(f"Processing {q['id']}...")
        
        expected_docs = q.get("expected_documents", [])
        if not expected_docs:
            answer = "No expected documents specified. Out of domain."
            pages = []
        else:
            context = get_pdf_text(expected_docs)
            
            # Truncate aggressively to prevent Groq 6000 TPM limit errors
            if len(context) > 15000:
                context = context[:15000]
                
            prompt = (
                "You are an expert HR and IT policy analyst. "
                "Based ONLY on the provided document context below, answer the following question. "
                "Keep your answer extremely concise, factual, and directly answering the question. "
                "If the answer is not in the context, explicitly say 'Information not found in the expected documents.'\n\n"
                f"CONTEXT:\n{context}\n\n"
                f"QUESTION: {q['question']}\n\n"
                "ANSWER:"
            )
            
            try:
                response = llm.invoke([
                    SystemMessage(content="You are a helpful and precise assistant."),
                    HumanMessage(content=prompt)
                ])
                answer = response.content.strip()
            except Exception as e:
                print(f"LLM Error on {q['id']}: {e}")
                answer = f"Error generating answer due to LLM failure: {str(e)}"

            pages = [] 
        
        # Remove any existing failed entry for this ID before appending
        ground_truth = [item for item in ground_truth if item["id"] != q["id"]]
        
        gt_entry = {
            "id": q["id"],
            "expected_answer": answer,
            "expected_documents": expected_docs,
            "expected_pages": pages
        }
        ground_truth.append(gt_entry)
        
        batch_count += 1
        if batch_count >= BATCH_SIZE:
            with open(CHECKPOINT_PATH, "w") as f:
                json.dump(ground_truth, f, indent=2)
            print(f"Checkpoint saved. Processed {len(ground_truth)} total.")
            batch_count = 0
            time.sleep(2) # Prevent rate limits between batches
        
        time.sleep(1.5) # Prevent rate limits per request

    # Final save
    if batch_count > 0:
        with open(CHECKPOINT_PATH, "w") as f:
            json.dump(ground_truth, f, indent=2)
        print(f"Final save completed. Processed {len(ground_truth)} total.")

if __name__ == "__main__":
    generate_ground_truth()
