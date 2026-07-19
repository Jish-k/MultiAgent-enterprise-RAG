import json
import os

QUESTIONS_PATH = "evaluation/dataset/questions.json"
OUTPUT_PATH = "evaluation/dataset/metadata.json"

def generate_metadata():
    with open(QUESTIONS_PATH, "r") as f:
        questions = json.load(f)

    metadata_list = []
    
    for q in questions:
        difficulty = q.get("difficulty", "Unknown")
        category = q.get("category", "Unknown")
        question_type = q.get("question_type", "Unknown")
        expected_docs = q.get("expected_documents", [])
        
        requires_reasoning = difficulty in ["Medium", "Hard", "Expert"]
        expected_document_count = len(expected_docs)
        requires_multiple_documents = (question_type in ["Comparison", "Multi Hop", "Comprehensive", "Cross Document"] or expected_document_count > 1)
        requires_verification = True
        requires_planning = True
        
        if expected_document_count <= 1:
            retrieval_difficulty = "Low"
        elif expected_document_count == 2:
            retrieval_difficulty = "Medium"
        else:
            retrieval_difficulty = "High"

        meta = {
            "id": q["id"],
            "difficulty": difficulty,
            "category": category,
            "question_type": question_type,
            "requires_reasoning": requires_reasoning,
            "requires_multiple_documents": requires_multiple_documents,
            "expected_document_count": expected_document_count,
            "requires_verification": requires_verification,
            "requires_planning": requires_planning,
            "retrieval_difficulty": retrieval_difficulty
        }
        metadata_list.append(meta)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(metadata_list, f, indent=2)
    print(f"Successfully generated metadata for {len(metadata_list)} questions.")

if __name__ == "__main__":
    generate_metadata()
