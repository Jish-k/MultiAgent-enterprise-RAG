import os
import sys
from orchestration.graph import AgenticRAGGraph

if __name__ == "__main__":
    print("Initializing pipeline...")
    pipeline = AgenticRAGGraph()
    print("Invoking pipeline...")
    try:
        state = pipeline.invoke("What is the capital of France?")
        print("Success!", state.keys())
    except Exception as e:
        import traceback
        traceback.print_exc()
