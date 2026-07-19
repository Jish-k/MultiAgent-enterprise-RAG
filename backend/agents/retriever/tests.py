import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from agents.retriever.agent import EvidenceRetrievalAgent

def test_retriever():
    print("Initializing Evidence Retrieval Agent...")
    agent = EvidenceRetrievalAgent()
    
    sub_queries = [
        "What is the process to apply for maternity leave?",
        "Who is the approval authority for maternity leave?",
        "Who approves maternity leave?" # Intentional near-duplicate query
    ]
    
    print(f"\nExecuting Multi-Query Search for:")
    for sq in sub_queries:
        print(f" - {sq}")
        
    package = agent.retrieve(request_id="test_001", sub_queries=sub_queries)
    
    print("\n--- Evidence Package Summary ---")
    print(f"Sources Used: {package.sources}")
    print(f"Chunks Retrieved: {package.retrieval_metrics.chunks_retrieved_total}")
    print(f"Duplicates Removed: {package.retrieval_metrics.duplicates_removed}")
    print(f"Final Chunk Count: {package.retrieval_metrics.chunks_after_dedup}")
    
    print("\n--- Latency Breakdown ---")
    print(f"Search: {package.retrieval_metrics.search_time_ms:.1f}ms")
    print(f"Merge:  {package.retrieval_metrics.merge_time_ms:.1f}ms")
    print(f"Dedup:  {package.retrieval_metrics.dedup_time_ms:.1f}ms")
    print(f"Rank:   {package.retrieval_metrics.ranking_time_ms:.1f}ms")
    print(f"Total:  {package.retrieval_metrics.total_time_ms:.1f}ms")
    
    print("\n--- Top 2 Ranked Chunks ---")
    for i, chunk in enumerate(package.chunks[:2], 1):
        print(f"\n{i}. [Score: {chunk.final_score:.3f}] {chunk.metadata.get('source')} (Page {chunk.metadata.get('page')})")
        print(f"Content Preview: {chunk.content[:150]}...")

if __name__ == "__main__":
    test_retriever()
