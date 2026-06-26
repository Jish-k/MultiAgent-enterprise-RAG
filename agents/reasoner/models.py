from pydantic import BaseModel, Field
from typing import List

class ReasonerMetrics(BaseModel):
    analysis_time_ms: float = 0.0
    generation_time_ms: float = 0.0
    total_time_ms: float = 0.0
    evidence_utilization_rate: float = 0.0

class ReasoningAnalysis(BaseModel):
    key_facts: List[str] = Field(default_factory=list)
    used_chunks: List[str] = Field(default_factory=list)
    discarded_chunks: List[str] = Field(default_factory=list)
    conflicts: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)

class ReasoningOutput(BaseModel):
    answer: str
    evidence_summary: str
    analysis: ReasoningAnalysis
    metrics: ReasonerMetrics = Field(default_factory=ReasonerMetrics)
