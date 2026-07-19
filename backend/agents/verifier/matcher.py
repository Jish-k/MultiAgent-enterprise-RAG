import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from embeddings.embedder import get_embedding_model
from agents.retriever.models import RankedChunk
from agents.verifier.models import SupportedClaim

class EvidenceMatcher:
    """
    Module 2: Deterministic Evidence Matcher.
    Matches extracted atomic claims against the used chunks via Cosine Similarity.
    """
    def __init__(self, threshold: float = 0.65):
        self.embedder = get_embedding_model()
        self.threshold = threshold
        
    def _cosine_similarity(self, a, b):
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return np.dot(a, b) / (norm_a * norm_b)
        
    def match(self, claims: list[str], chunks: list[RankedChunk]) -> tuple[list[SupportedClaim], list[str]]:
        if not claims:
            return [], []
        if not chunks:
            return [], claims
            
        supported = []
        unsupported = []
        
        chunk_texts = [c.content for c in chunks]
        chunk_embeddings = self.embedder.embed_documents(chunk_texts)
        claim_embeddings = self.embedder.embed_documents(claims)
        
        for i, claim in enumerate(claims):
            claim_emb = claim_embeddings[i]
            
            best_score = -1.0
            best_chunk = None
            
            for j, chunk_emb in enumerate(chunk_embeddings):
                score = self._cosine_similarity(claim_emb, chunk_emb)
                if score > best_score:
                    best_score = score
                    best_chunk = chunks[j]
                    
            if best_score >= self.threshold:
                supported.append(SupportedClaim(
                    claim=claim,
                    chunk_id=best_chunk.chunk_id,
                    similarity_score=float(best_score)
                ))
            else:
                unsupported.append(claim)
                
        return supported, unsupported
