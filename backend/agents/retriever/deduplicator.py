import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from embeddings.embedder import get_embedding_model

def cosine_similarity(vec1, vec2):
    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

def deduplicate_chunks(merged_results: list[dict], threshold: float = 0.95) -> tuple[list[dict], int]:
    """
    Uses Sentence Transformer embeddings to find and drop semantically near-duplicate chunks.
    Returns the deduplicated list and the count of duplicates removed.
    """
    if not merged_results:
        return [], 0
        
    embeddings_model = get_embedding_model()
    
    texts = [item["document"].page_content for item in merged_results]
    embeddings = embeddings_model.embed_documents(texts)
    
    # Sort by score descending to prioritize keeping high-quality retrievals
    paired = list(zip(merged_results, embeddings))
    paired.sort(key=lambda x: x[0]["score"], reverse=True)
    
    unique_results = []
    unique_embeddings = []
    duplicates_removed = 0
    
    for item, emb in paired:
        is_duplicate = False
        for u_emb in unique_embeddings:
            sim = cosine_similarity(emb, u_emb)
            if sim >= threshold:
                is_duplicate = True
                duplicates_removed += 1
                break
                
        if not is_duplicate:
            unique_results.append(item)
            unique_embeddings.append(emb)
            
    return unique_results, duplicates_removed
