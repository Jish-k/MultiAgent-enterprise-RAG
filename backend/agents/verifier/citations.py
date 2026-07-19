import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from agents.verifier.models import SupportedClaim
from agents.retriever.models import RankedChunk

class CitationGenerator:
    """
    Module 4: Deterministic Citation Generator.
    Maps supported claims back to their source chunks and formats the metadata.
    """
    
    def generate(self, supported_claims: list[SupportedClaim], used_chunks: list[RankedChunk]) -> list[str]:
        citations = set()
        
        chunk_dict = {c.chunk_id: c for c in used_chunks}
        
        for claim in supported_claims:
            chunk = chunk_dict.get(claim.chunk_id)
            if chunk:
                doc = getattr(chunk, "document", "Unknown Document")
                page = getattr(chunk, "page", "Unknown Page")
                section = getattr(chunk, "section", "Unknown Section")
                
                citation = f"{doc}, Page {page}, Section: {section}"
                citations.add(citation)
                
        return list(citations)
