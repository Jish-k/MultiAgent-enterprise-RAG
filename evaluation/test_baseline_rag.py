import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rag.pipeline import BaselineRAG

test_queries = [
    {"category": "HR Policies", "query": "How many casual leaves are employees entitled to each year?"},
    {"category": "HR Policies", "query": "What is the maternity leave policy?"},
    {"category": "HR Policies", "query": "What is the notice period for resignation?"},
    {"category": "IT Policies", "query": "What are the password requirements?"},
    {"category": "IT Policies", "query": "Can employees use personal USB drives?"},
    {"category": "Travel Policies", "query": "How can employees claim travel expenses?"},
    {"category": "Travel Policies", "query": "Who approves business travel?"},
    {"category": "Complex Queries", "query": "How do I apply for maternity leave and who approves it?"},
    {"category": "Complex Queries", "query": "Can I work remotely while on probation?"},
    {"category": "Complex Queries", "query": "What happens if I violate the company's IT security policy?"}
]

def run_evaluation():
    print("Initializing Baseline RAG Engine (Groq Backend)...")
    try:
        rag = BaselineRAG()
    except ValueError as e:
        print(f"\n[ERROR] Initialization failed: {e}")
        print("Please ensure you have added your GROQ_API_KEY to the .env file.")
        return

    report = "# Phase 5: Baseline RAG Evaluation Report\n\n"
    
    for i, test in enumerate(test_queries, 1):
        cat = test["category"]
        query = test["query"]
        
        print(f"\n[{i}/10] Testing [{cat}]: {query}")
        
        # We also want to manually retrieve the documents to verify retrieval
        from rag.retriever import get_rag_retriever
        retriever = get_rag_retriever()
        docs = retriever.invoke(query)
        sources = list(set([doc.metadata.get("source", "Unknown") for doc in docs]))
        
        # Generate the Answer
        answer = rag.ask(query)
        
        report += f"### Q{i}: {query}\n"
        report += f"**Category:** {cat}\n\n"
        report += f"**Retrieved Sources:** {', '.join(sources)}\n\n"
        report += f"**LLM Answer:**\n{answer}\n\n"
        report += "---\n"
        
    # Write to artifact
    with open("baseline_rag_report.md", "w") as f:
        f.write(report)
        
    print("\nEvaluation Complete! Results saved to baseline_rag_report.md")

if __name__ == "__main__":
    run_evaluation()
