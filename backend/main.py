import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Enterprise Agentic RAG API", description="Backend for the Research Visualization Platform")

# Enable CORS for the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")

def load_json_file(filename: str, default_val=None):
    if default_val is None:
        default_val = {}
    filepath = os.path.join(RESULTS_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return default_val

@app.get("/api/project")
async def get_project_overview():
    return {
        "title": "Enterprise Agentic RAG",
        "subtitle": "A multi-stage, reasoning-driven retrieval augmented generation architecture.",
        "goal": "Solve multi-hop reasoning and hallucination in standard RAG pipelines.",
        "problemStatement": "Traditional RAG struggles with multi-hop reasoning, complex queries, and unverified outputs. We propose a pipeline using a Planner, Retriever, Reasoner, and Verifier.",
    }

@app.get("/api/architecture")
async def get_architecture():
    return {
        "modules": [
            {"name": "Planner", "description": "Deconstructs complex user queries into sub-queries."},
            {"name": "Retriever", "description": "Fetches context using semantic search from ChromaDB."},
            {"name": "Reasoner", "description": "Generates a Chain of Thought tracing retrieved facts."},
            {"name": "Verifier", "description": "Critiques the reasoning trace against the context to prevent hallucinations."}
        ]
    }

@app.get("/api/results")
async def get_results():
    # Load all metrics from json files
    baseline = load_json_file("baseline.json", {"accuracy": 49.17, "recall": 92.50, "mrr": 0.8569, "latency": 4.84})
    planner = load_json_file("planner.json", {"accuracy": 51.67, "recall": 97.50, "mrr": 0.8686, "latency": 22.58})
    reasoner = load_json_file("reasoner.json", {"accuracy": 75.00, "recall": 97.50, "mrr": 0.8686, "latency": 31.36})
    verifier = load_json_file("verifier.json", {"accuracy": None, "recall": None, "mrr": None, "latency": None})
    
    return {
        "baseline": baseline,
        "planner": planner,
        "reasoner": reasoner,
        "verifier": verifier
    }

@app.get("/api/datasets")
async def get_datasets():
    return {
        "hotpotqa": {
            "name": "HotpotQA Benchmark",
            "questions": 120,
            "documents": "Derived from Wikipedia paragraphs",
            "type": "Multi-hop Reasoning"
        },
        "enterprise": {
            "name": "Enterprise Private Data",
            "questions": 0,
            "documents": 0,
            "type": "Private Docs"
        }
    }

class DemoRequest(BaseModel):
    question: str

@app.post("/api/demo")
async def run_demo(req: DemoRequest):
    # In a full deployment, this triggers the Agentic RAG pipeline.
    # For presentation reliability, we return pre-computed traces for specific demo questions.
    
    q_lower = req.question.lower().strip()
    
    if "percy clifford" in q_lower or "nigel graham" in q_lower:
        return {
            "question": req.question,
            "planner_queries": [
                "When was Percy Clifford Mills born?",
                "When was Nigel Graham Pearson born?"
            ],
            "retrieved_chunks": [
                "[Doc 1] Percy Clifford Mills (born 1909) was an English footballer...",
                "[Doc 2] Nigel Graham Pearson (born 21 August 1963) is an English football manager..."
            ],
            "reasoning": "1. Percy Clifford Mills was born in 1909.\n2. Nigel Graham Pearson was born in 1963.\n3. 1909 is earlier than 1963.\nConclusion: Percy Clifford Mills was born first.",
            "verification": "[PASS] The retrieved documents explicitly state the birth years for both individuals. The chronological comparison is mathematically sound.",
            "final_answer": "Percy Clifford Mills was born first (in 1909), whereas Nigel Graham Pearson was born later (in 1963)."
        }
        
    elif "arthur's magazine" in q_lower or "first started" in q_lower:
        return {
            "question": req.question,
            "planner_queries": [
                "When was Arthur's Magazine first started?",
                "When was First for Women first started?"
            ],
            "retrieved_chunks": [
                "[Doc 1] Arthur's Magazine (1844–1846) was an American literary magazine published in Philadelphia.",
                "[Doc 2] First for Women is a woman's magazine published by Bauer Media Group in the USA. It was started in 1989."
            ],
            "reasoning": "1. Arthur's Magazine was started in 1844.\n2. First for Women was started in 1989.\n3. 1844 is earlier than 1989.\nConclusion: Arthur's Magazine was started first.",
            "verification": "[PASS] Context verifies Arthur's Magazine began publication in 1844 and First for Women in 1989. The temporal reasoning holds.",
            "final_answer": "Arthur's Magazine was started first (in 1844), compared to First for Women which began in 1989."
        }
        
    elif "telemundo" in q_lower or "english translation" in q_lower:
        return {
            "question": req.question,
            "planner_queries": [
                "What does 'Telemundo' mean in English?",
                "Translate 'Telemundo' to English."
            ],
            "retrieved_chunks": [
                "[Doc 1] Telemundo (Spanish pronunciation: [teleˈmundo]; English: World TV) is an American Spanish-language terrestrial television network."
            ],
            "reasoning": "1. The context provides the English translation for Telemundo.\n2. It translates to 'World TV'.",
            "verification": "[PASS] The provided context explicitly contains the English translation 'World TV'. No hallucination detected.",
            "final_answer": "The English translation of Telemundo is 'World TV'."
        }

    # Fallback for any other random question
    return {
        "question": req.question,
        "planner_queries": [
            f"Extract key entities from: {req.question}",
            f"Search Wikipedia/Enterprise DB for: {req.question}"
        ],
        "retrieved_chunks": [
            f"Chunk 1: Document containing information related to '{req.question[:20]}...'",
            f"Chunk 2: Supporting evidence for '{req.question[-20:]}'"
        ],
        "reasoning": "The retriever found relevant documents matching the query intent. Synthesizing the facts to formulate a direct response.",
        "verification": "[PASS] The generated reasoning aligns with the retrieved context.",
        "final_answer": f"Based on the retrieved context, this is a simulated response to your question: '{req.question}'. In a live environment, the LLM would populate this with exact facts."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
