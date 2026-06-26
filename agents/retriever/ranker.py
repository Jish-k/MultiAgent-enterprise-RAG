import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from agents.retriever.models import RankedChunk

def rank_evidence(unique_results: list[dict], planner_confidence: float = 1.0, weights: dict = None) -> list[RankedChunk]:
    """
    Ranks the deduplicated chunks using a configurable hybrid scoring mechanism.
    """
    if weights is None:
        weights = {
            "retrieval_similarity": 0.6,
            "planner_confidence": 0.4
        }
        
    ranked_chunks = []
    
    for item in unique_results:
        doc = item["document"]
        sim_score = item["score"]
        
        final_score = (weights["retrieval_similarity"] * sim_score) + (weights["planner_confidence"] * planner_confidence)
        
        chunk = RankedChunk(
            chunk_id=str(uuid.uuid4())[:8],
            content=doc.page_content,
            document=doc.metadata.get("source", "Unknown").split("/")[-1],
            page=doc.metadata.get("page", 0),
            section=doc.metadata.get("section", "Unknown"),
            metadata=doc.metadata,
            retrieval_similarity=sim_score,
            planner_confidence=planner_confidence,
            final_score=final_score
        )
        ranked_chunks.append(chunk)
        
    # Sort by final score descending
    ranked_chunks.sort(key=lambda x: x.final_score, reverse=True)
    return ranked_chunks
