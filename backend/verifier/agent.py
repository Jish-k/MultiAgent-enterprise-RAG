import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from verifier.models import VerifiedResponse, VerificationMetrics
from verifier.claim_extractor import ClaimExtractor
from verifier.matcher import EvidenceMatcher
from verifier.confidence import ConfidenceCalculator
from verifier.citations import CitationGenerator
from retriever.models import RankedChunk
from llm.provider import get_llm

from config import Config

class VerifierAgent:
    """
    Agent 4: The Verifier Agent.
    Validates claims deterministically, computes ESS, and generates citations.
    """
    def __init__(self, threshold: float = 0.50, api_key: str = None, anthropic_api_key: str = None, llm_provider: str = Config.LLM_PROVIDER):
        self.llm = get_llm(api_key=api_key, anthropic_api_key=anthropic_api_key, llm_provider=llm_provider)
        self.extractor = ClaimExtractor(llm=self.llm)
        self.matcher = EvidenceMatcher(threshold=threshold)
        self.calculator = ConfidenceCalculator()
        self.citator = CitationGenerator()
        
    def verify(self, 
               question: str,
               draft_answer: str, 
               used_chunks: list[RankedChunk],
               required_information: list[str]) -> VerifiedResponse:
               
        start_time = time.time()
        
        # 1. Extract Claims (LLM)
        ext_start = time.time()
        claims = self.extractor.extract(draft_answer, question)
        ext_time = (time.time() - ext_start) * 1000
        
        # 2. Match Evidence (Independent Retrieval + Deterministic Matching)
        match_start = time.time()
        
        from rag.retriever import get_rag_retriever
        retriever = get_rag_retriever()
        
        independent_chunks = []
        seen_chunk_ids = set()
        
        for claim in claims:
            # Retrieve fresh evidence for each claim
            retrieved = retriever.invoke(claim)
            for chunk in retrieved:
                chunk_id = chunk.metadata.get('id', chunk.page_content[:50])
                if chunk_id not in seen_chunk_ids:
                    seen_chunk_ids.add(chunk_id)
                    independent_chunks.append(chunk)
                    
        # Verify claims against the independently retrieved chunks instead of original context
        supported_claims, unsupported_claims = self.matcher.match(claims, independent_chunks)
        match_time = (time.time() - match_start) * 1000
        
        # 3. Calculate Confidence and ESS
        confidence, ess = self.calculator.calculate(
            supported_claims=supported_claims,
            total_claims=len(claims),
            used_chunks=independent_chunks,
            required_info=required_information
        )
        
        # 4. Generate Citations
        citations = self.citator.generate(supported_claims, independent_chunks)
        
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
