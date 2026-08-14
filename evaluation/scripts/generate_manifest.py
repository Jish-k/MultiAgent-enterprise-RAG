import os
import json
import subprocess
from datetime import datetime

def get_git_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
    except:
        return "unknown_or_not_git_repo"

def generate_manifest():
    manifest = {
      "experiment_name": "Pilot Benchmark",
      "experiment_version": "1.0",
      "dataset_version": "1.0",
      "pipeline_version": "1.0",
      "benchmark_commit": get_git_commit(),
      "llm": {
          "provider": "Groq",
          "model": "llama-3.1-8b",
          "temperature": 0.0
      },
      "embedding_model": "all-MiniLM-L6-v2",
      "vector_db": "ChromaDB",
      "retrieval": {
          "top_k": 5,
          "chunk_size": 500,
          "chunk_overlap": 50
      },
      "runs_per_configuration": 3,
      "configurations": [
          "Baseline (Config A)",
          "Planner (Config B)",
          "Planner+Reasoner (Config D)",
          "Full Agentic (Config C)"
      ],
      "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    out_dir = "evaluation/results/pilot"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "experiment_manifest.json")
    
    with open(out_path, "w") as f:
        json.dump(manifest, f, indent=2)
        
    print(f"Generated manifest at {out_path}")

if __name__ == "__main__":
    generate_manifest()
