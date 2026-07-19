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
    # In a real implementation, this would import the RAG pipeline and stream the result.
    # For now, we return a mock response that demonstrates the structure.
    return {
        "question": req.question,
        "planner_queries": [
            "What is X?",
            "How does X relate to Y?"
        ],
        "retrieved_chunks": [
            "Chunk 1 discussing X",
            "Chunk 2 discussing Y"
        ],
        "reasoning": "Since Chunk 1 says X and Chunk 2 says Y, X is related to Y.",
        "verification": "The reasoning is factually supported by Chunk 1 and 2.",
        "final_answer": "X is related to Y because..."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
