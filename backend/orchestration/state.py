from typing import TypedDict, Optional, List, Dict, Any
from retriever.models import EvidencePackage
from reasoner.models import ReasoningOutput
from verifier.models import VerifiedResponse

class AgenticRAGState(TypedDict):
    request_id: str
    question: str
    
    # Planner outputs
    intent: Optional[str]
    complexity: Optional[str]
    sub_queries: List[str]
    required_information: List[str]
    planner_metrics: Dict[str, Any]
    
    # Retriever outputs
    evidence_package: Optional[EvidencePackage]
    
    # Reasoner outputs
    reasoning_output: Optional[ReasoningOutput]
    
    # Verifier outputs
    verifier_response: Optional[VerifiedResponse]
    final_answer: str
