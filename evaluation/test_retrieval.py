import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from embeddings.retrieval import get_retriever

test_queries = [
    {"query": "How many casual leaves are allowed?", "expected_doc": "Leave_Policy.pdf"},
    {"query": "What is the notice period?", "expected_doc": "Employee_Handbook.pdf"}, # Resignation info is in handbook
    {"query": "How should passwords be created?", "expected_doc": "IT_Security.pdf"},
    {"query": "Can employees work remotely?", "expected_doc": "Employee_Handbook.pdf"}, # Remote work is in handbook
    {"query": "How are travel expenses reimbursed?", "expected_doc": "Travel_Policy.pdf"},
    {"query": "What is the company vision?", "expected_doc": "Employee_Handbook.pdf"},
    {"query": "How many sick leaves do I get?", "expected_doc": "Leave_Policy.pdf"},
    {"query": "Can I bring my own laptop?", "expected_doc": "IT_Security.pdf"},
    {"query": "Who approves international travel?", "expected_doc": "Travel_Policy.pdf"},
    {"query": "What is the dress code?", "expected_doc": "Employee_Handbook.pdf"},
    {"query": "Are interns allowed to work remotely?", "expected_doc": "Employee_Handbook.pdf"},
    {"query": "What is the maternity leave duration?", "expected_doc": "Leave_Policy.pdf"},
    {"query": "What happens if I lose my laptop?", "expected_doc": "IT_Security.pdf"},
    {"query": "What is the daily food allowance for domestic travel?", "expected_doc": "Travel_Policy.pdf"},
    {"query": "How do I report a security incident?", "expected_doc": "IT_Security.pdf"},
    {"query": "What are the core collaboration hours?", "expected_doc": "Employee_Handbook.pdf"},
    {"query": "When does probation end?", "expected_doc": "Employee_Handbook.pdf"},
    {"query": "How many days of earned leave can I carry forward?", "expected_doc": "Leave_Policy.pdf"},
    {"query": "What is the hotel cap for Tier-1 cities?", "expected_doc": "Travel_Policy.pdf"},
    {"query": "What is the training budget?", "expected_doc": "Employee_Handbook.pdf"},
]

def run_validation():
    print("Initializing Retriever (k=3)...")
    retriever = get_retriever(k=3)
    
    correct_retrievals = 0
    total_queries = len(test_queries)
    
    results_markdown = "# Retrieval Validation Report\n\n"
    results_markdown += f"**Total Queries Evaluated:** {total_queries}\n\n"
    results_markdown += "## Query Breakdown\n\n"
    results_markdown += "| No. | Query | Expected Document | Top Retrieved Document | Match? | Metadata (Page) |\n"
    results_markdown += "|---|---|---|---|---|---|\n"
    
    print(f"Running {total_queries} test queries...")
    
    for i, test in enumerate(test_queries, 1):
        query = test["query"]
        expected = test["expected_doc"]
        
        # Retrieve documents
        docs = retriever.invoke(query)
        
        # Check if expected document is in the top 3
        # Also check what the #1 document was
        retrieved_sources = [doc.metadata.get("source") for doc in docs]
        top_source = retrieved_sources[0] if retrieved_sources else "None"
        top_page = docs[0].metadata.get("page_number") if docs else "N/A"
        
        # We consider it a success if the expected doc is in the top 3
        # But we'll track if it hit #1 specifically for strict scoring
        is_match = expected in retrieved_sources
        if is_match:
            correct_retrievals += 1
            match_str = "✅ Yes"
        else:
            match_str = "❌ No"
            
        results_markdown += f"| {i} | {query} | {expected} | {top_source} | {match_str} | Page {top_page} |\n"
        
    accuracy = (correct_retrievals / total_queries) * 100
    
    results_markdown += f"\n## Final Score\n\n"
    results_markdown += f"**Accuracy:** {accuracy:.1f}%\n"
    results_markdown += f"**Target:** 80-90%\n"
    
    if accuracy >= 80:
        results_markdown += "> [!TIP]\n> **Status: PASSED**. The retriever meets the reliability threshold and is ready for LLM integration.\n"
    else:
        results_markdown += "> [!WARNING]\n> **Status: FAILED**. The retriever did not meet the 80% accuracy threshold. We may need to tweak chunking or use a different embedding model.\n"
        
    # Write report to artifact
    with open("retrieval_validation_report.md", "w") as f:
        f.write(results_markdown)
        
    print(f"\nValidation Complete! Accuracy: {accuracy:.1f}%")
    print("Report written to retrieval_validation_report.md")

if __name__ == "__main__":
    run_validation()
