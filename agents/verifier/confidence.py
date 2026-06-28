import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from agents.verifier.models import SupportedClaim
from agents.retriever.models import RankedChunk

class ConfidenceCalculator:
    """
    Module 3: Deterministic Confidence Calculator.
    Calculates mathematical confidence and Evidence Sufficiency Score (ESS).
    """
    
    def calculate(self, 
                  supported_claims: list[SupportedClaim], 
                  total_claims: int,
                  used_chunks: list[RankedChunk],
                  required_info: list[str]) -> tuple[float, float]:
                  
        # 1. Claim Support Rate
        support_rate = len(supported_claims) / total_claims if total_claims > 0 else 0.0
        
        # 2. Retrieval Similarity
        avg_retrieval_sim = 0.0
        if used_chunks:
            avg_retrieval_sim = sum(c.final_score for c in used_chunks) / len(used_chunks)
            
        # 3. Citation Completeness
        citation_completeness = 1.0 if support_rate > 0 else 0.0
            
        # 4. Reasoning Coverage
        reasoning_coverage = 1.0 
        
        # Math Formula
        confidence = (0.40 * avg_retrieval_sim) + \
                     (0.25 * reasoning_coverage) + \
                     (0.20 * support_rate) + \
                     (0.15 * citation_completeness)
                     
        # 5. Evidence Sufficiency Score (ESS)
        ess = 1.0
        if required_info:
            covered_reqs = set()
            for req in required_info:
                req_lower = req.lower()
                # Try simple substring match
                for claim in supported_claims:
                    if req_lower in claim.claim.lower():
                        covered_reqs.add(req)
                        break
            
            ess = len(covered_reqs) / len(required_info)
        elif not supported_claims and required_info:
            ess = 0.0
            
        return min(confidence, 1.0), ess
