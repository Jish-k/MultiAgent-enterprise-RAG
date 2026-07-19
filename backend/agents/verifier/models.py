from pydantic import BaseModel, Field
from typing import List

class VerificationMetrics(BaseModel):
    claim_support_rate: float = 0.0
    citation_accuracy: float = 1.0
    unsupported_claim_count: int = 0
    average_confidence: float = 0.0
    evidence_sufficiency_score: float = 0.0
    extraction_time_ms: float = 0.0
    matching_time_ms: float = 0.0
    total_time_ms: float = 0.0

class SupportedClaim(BaseModel):
    claim: str
    chunk_id: str
    similarity_score: float

class VerifiedResponse(BaseModel):
    answer: str
    confidence: float
    citations: List[str] = Field(default_factory=list)
    claims: List[str] = Field(default_factory=list)
    supported_claims: List[SupportedClaim] = Field(default_factory=list)
    unsupported_claims: List[str] = Field(default_factory=list)
    verification_metrics: VerificationMetrics = Field(default_factory=VerificationMetrics)
