import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rag.generator import build_rag_chain

class BaselineRAG:
    def __init__(self):
        print("Building Baseline RAG Engine...")
        self.chain = build_rag_chain()
        print("RAG Engine ready!")
        
    def ask(self, question: str) -> str:
        """
        Executes the RAG pipeline for a given question.
        """
        print(f"\n[?] Question: {question}")
        try:
            answer = self.chain.invoke(question)
            print(f"\n[!] Answer: \n{answer}\n")
            return answer
        except Exception as e:
            error_msg = f"Error during RAG execution: {str(e)}"
            print(error_msg)
            return error_msg

if __name__ == "__main__":
    # Quick test of the pipeline
    rag = BaselineRAG()
    rag.ask("What is the daily food allowance for domestic travel?")
