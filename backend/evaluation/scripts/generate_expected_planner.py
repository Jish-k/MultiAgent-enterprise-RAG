import json
import os
import time
import sys
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from llm.provider import get_llm

QUESTIONS_PATH = "evaluation/dataset/questions.json"
CHECKPOINT_PATH = "evaluation/dataset/expected_planner.json"
BATCH_SIZE = 20

class PlannerGroundTruth(BaseModel):
    intent: str = Field(description="The main topic or intent of the question, e.g. leave_policy, it_security")
    complexity: str = Field(description="The complexity of the query: 'single_hop', 'multi_hop', 'comparison', 'comprehensive', or 'out_of_domain'")
    required_information: list[str] = Field(description="List of atomic information required to answer the question")
    retrieval_strategy: str = Field(description="The strategy to use: 'single_document' or 'multi_document' or 'none'")

def generate_expected_planner():
    with open(QUESTIONS_PATH, "r") as f:
        questions = json.load(f)

    if os.path.exists(CHECKPOINT_PATH):
        with open(CHECKPOINT_PATH, "r") as f:
            planner_gt = json.load(f)
    else:
        planner_gt = []

    processed_ids = {item["id"] for item in planner_gt}
    llm = get_llm()
    
    batch_count = 0
    for q in questions:
        if q["id"] in processed_ids:
            continue
            
        print(f"Processing Planner GT for {q['id']}...")
        
        prompt = (
            "Analyze the following question and determine the required planning information. "
            "Output EXACTLY and ONLY valid JSON with no markdown formatting. The JSON must have these keys:\n"
            "- intent (string): The main topic (e.g. leave_policy, it_security)\n"
            "- complexity (string): 'single_hop', 'multi_hop', 'comparison', 'comprehensive', or 'out_of_domain'\n"
            "- required_information (array of strings): List of atomic information required to answer\n"
            "- retrieval_strategy (string): 'single_document', 'multi_document', or 'none'\n\n"
            f"Question: {q['question']}"
        )
        
        try:
            result_str = llm.invoke([
                SystemMessage(content="You are an expert intent classifier. You always output raw, valid JSON."),
                HumanMessage(content=prompt)
            ]).content.strip()
            
            # Clean up potential markdown formatting
            if result_str.startswith("```json"):
                result_str = result_str[7:]
            if result_str.startswith("```"):
                result_str = result_str[3:]
            if result_str.endswith("```"):
                result_str = result_str[:-3]
                
            result_data = json.loads(result_str.strip())
            
            entry = {
                "id": q["id"],
                "intent": result_data.get("intent", "unknown"),
                "complexity": result_data.get("complexity", "unknown"),
                "required_information": result_data.get("required_information", []),
                "retrieval_strategy": result_data.get("retrieval_strategy", "unknown"),
                "expected_documents": q.get("expected_documents", [])
            }
        except Exception as e:
            print(f"LLM Error on {q['id']}: {e}")
            entry = {
                "id": q["id"],
                "intent": "unknown",
                "complexity": "unknown",
                "required_information": [],
                "retrieval_strategy": "unknown",
                "expected_documents": q.get("expected_documents", [])
            }
        
        planner_gt.append(entry)
        
        batch_count += 1
        if batch_count >= BATCH_SIZE:
            with open(CHECKPOINT_PATH, "w") as f:
                json.dump(planner_gt, f, indent=2)
            print(f"Checkpoint saved. Processed {len(planner_gt)} total.")
            batch_count = 0
            time.sleep(2)
        
        time.sleep(1.5)

    if batch_count > 0:
        with open(CHECKPOINT_PATH, "w") as f:
            json.dump(planner_gt, f, indent=2)
        print(f"Final save completed. Processed {len(planner_gt)} total.")

if __name__ == "__main__":
    generate_expected_planner()
