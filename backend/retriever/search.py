import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from embeddings.vector_store import get_vector_store

def execute_multi_search(sub_queries: list[str], k: int = 3) -> list[dict]:
    """
    Executes a search against the ChromaDB vector store for each sub-query.
    Returns a list of dictionaries containing the Document, relevance score, and source query.
    """
    vector_store = get_vector_store()
    raw_results = []
    
    for query in sub_queries:
        try:
            # Returns List[Tuple[Document, float]]
            results = vector_store.similarity_search_with_relevance_scores(query, k=k)
            for doc, score in results:
                raw_results.append({
                    "document": doc,
                    "score": score,
                    "source_query": query
                })
        except Exception as e:
            print(f"[Search Warning] Query failed: {query} -> {e}")
            
    return raw_results
