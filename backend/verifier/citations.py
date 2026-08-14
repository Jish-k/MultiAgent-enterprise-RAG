import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from verifier.models import SupportedClaim
from retriever.models import RankedChunk

class CitationGenerator:
    """
    Module 4: Deterministic Citation Generator.
    Maps supported claims back to their source chunks and formats the metadata.
    """
    
    def generate(self, supported_claims: list[SupportedClaim], used_chunks: list[RankedChunk]) -> list[str]:
        citations = set()
        
        chunk_dict = {getattr(c, 'chunk_id', c.metadata.get('id', 'unknown') if hasattr(c, 'metadata') else 'unknown'): c for c in used_chunks}
        
        for claim in supported_claims:
            chunk = chunk_dict.get(claim.chunk_id)
            if chunk:
                if hasattr(chunk, 'metadata'):
                    doc = chunk.metadata.get("source", "Unknown Document")
                    page = chunk.metadata.get("page_number", "Unknown Page")
                    section = chunk.metadata.get("section", "Unknown Section")
                else:
                    doc = getattr(chunk, "document", "Unknown Document")
                    page = getattr(chunk, "page", "Unknown Page")
                    section = getattr(chunk, "section", "Unknown Section")
                
                citation = f"{doc}, Page {page}, Section: {section}"
                citations.add(citation)
                
        return list(citations)
