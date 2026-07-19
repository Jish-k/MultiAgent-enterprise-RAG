import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.verifier.models import VerifiedResponse, VerificationMetrics
from agents.verifier.claim_extractor import ClaimExtractor
from agents.verifier.matcher import EvidenceMatcher
from agents.verifier.confidence import ConfidenceCalculator
from agents.verifier.citations import CitationGenerator
from agents.retriever.models import RankedChunk

class VerifierAgent:
    """
    Agent 4: The Verifier Agent.
    Validates claims deterministically, computes ESS, and generates citations.
    """
    def __init__(self, threshold: float = 0.65):
        self.extractor = ClaimExtractor()
        self.matcher = EvidenceMatcher(threshold=threshold)
        self.calculator = ConfidenceCalculator()
        self.citator = CitationGenerator()
        
    def verify(self, 
               draft_answer: str, 
               used_chunks: list[RankedChunk],
               required_information: list[str]) -> VerifiedResponse:
               
        start_time = time.time()
        
        # 1. Extract Claims (LLM)
        ext_start = time.time()
        claims = self.extractor.extract(draft_answer)
        ext_time = (time.time() - ext_start) * 1000
        
        # 2. Match Evidence (Deterministic)
        match_start = time.time()
        supported_claims, unsupported_claims = self.matcher.match(claims, used_chunks)
        match_time = (time.time() - match_start) * 1000
        
        # 3. Calculate Confidence and ESS
        confidence, ess = self.calculator.calculate(
            supported_claims=supported_claims,
            total_claims=len(claims),
            used_chunks=used_chunks,
            required_info=required_information
        )
        
        # 4. Generate Citations
        citations = self.citator.generate(supported_claims, used_chunks)
        
        total_time = (time.time() - start_time) * 1000
        
        # Assemble Response
        metrics = VerificationMetrics(
            claim_support_rate=len(supported_claims) / len(claims) if claims else 0.0,
            citation_accuracy=1.0, 
            unsupported_claim_count=len(unsupported_claims),
            average_confidence=confidence,
            evidence_sufficiency_score=ess,
            extraction_time_ms=ext_time,
            matching_time_ms=match_time,
            total_time_ms=total_time
        )
        
        return VerifiedResponse(
            answer=draft_answer,
            confidence=confidence,
            citations=citations,
            claims=claims,
            supported_claims=supported_claims,
            unsupported_claims=unsupported_claims,
            verification_metrics=metrics
        )
