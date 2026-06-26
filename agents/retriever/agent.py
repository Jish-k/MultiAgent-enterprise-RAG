import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from agents.retriever.models import EvidencePackage, RetrievalMetrics
from agents.retriever.search import execute_multi_search
from agents.retriever.merger import merge_results
from agents.retriever.deduplicator import deduplicate_chunks
from agents.retriever.ranker import rank_evidence

class EvidenceRetrievalAgent:
    """
    Agent 2: The Evidence Retrieval Agent.
    Executes sub-queries, merges results, removes duplicates semantically, and ranks the evidence.
    """
    
    def retrieve(self, request_id: str, sub_queries: list[str], planner_confidence: float = 1.0) -> EvidencePackage:
        metrics = RetrievalMetrics()
        
        # 1. Search
        start = time.time()
        raw_results = execute_multi_search(sub_queries, k=3)
        metrics.search_time_ms = (time.time() - start) * 1000
        metrics.chunks_retrieved_total = len(raw_results)
        
        # 2. Merge Exact Matches
        start = time.time()
        merged_results = merge_results(raw_results)
        metrics.merge_time_ms = (time.time() - start) * 1000
        
        # 3. Deduplicate Semantic Matches
        start = time.time()
        unique_results, duplicates_removed = deduplicate_chunks(merged_results, threshold=0.95)
        metrics.dedup_time_ms = (time.time() - start) * 1000
        metrics.duplicates_removed = (len(raw_results) - len(merged_results)) + duplicates_removed
        metrics.chunks_after_dedup = len(unique_results)
        
        # 4. Rank
        start = time.time()
        ranked_chunks = rank_evidence(unique_results, planner_confidence)
        metrics.ranking_time_ms = (time.time() - start) * 1000
        
        metrics.total_time_ms = metrics.search_time_ms + metrics.merge_time_ms + metrics.dedup_time_ms + metrics.ranking_time_ms
        
        # Extract unique sources
        sources = list(set([chunk.metadata.get("source", "Unknown") for chunk in ranked_chunks]))
        
        return EvidencePackage(
            request_id=request_id,
            chunks=ranked_chunks,
            sources=sources,
            retrieval_metrics=metrics
        )
