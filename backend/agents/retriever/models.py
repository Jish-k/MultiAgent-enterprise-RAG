from pydantic import BaseModel, Field
from typing import List, Dict, Any

class RetrievalMetrics(BaseModel):
    search_time_ms: float = 0.0
    merge_time_ms: float = 0.0
    dedup_time_ms: float = 0.0
    ranking_time_ms: float = 0.0
    total_time_ms: float = 0.0
    chunks_retrieved_total: int = 0
    duplicates_removed: int = 0
    chunks_after_dedup: int = 0

class RankedChunk(BaseModel):
    chunk_id: str
    content: str
    document: str
    page: int
    section: str = "Unknown"
    metadata: Dict[str, Any]
    retrieval_similarity: float
    planner_confidence: float = 1.0
    final_score: float

class EvidencePackage(BaseModel):
    request_id: str = Field(default_factory=lambda: "req_000")
    chunks: List[RankedChunk] = []
    sources: List[str] = []
    retrieval_metrics: RetrievalMetrics = Field(default_factory=RetrievalMetrics)
