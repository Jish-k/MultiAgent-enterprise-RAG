from .vector_store import get_vector_store

def get_retriever(search_type="similarity", k=4):
    """
    Returns a configured retriever from the vector database.
    """
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(
        search_type=search_type,
        search_kwargs={"k": k}
    )
    return retriever

def test_retrieval(query):
    """Simple test function to verify retrieval works."""
    print(f"\nSearching for: '{query}'")
    retriever = get_retriever(k=2)
    results = retriever.invoke(query)
    
    for i, doc in enumerate(results, 1):
        print(f"\n--- Result {i} ---")
        print(f"Source: {doc.metadata.get('source')} (Page {doc.metadata.get('page_number')})")
        print(f"Section: {doc.metadata.get('section')}")
        print(f"Content snippet: {doc.page_content[:150]}...")
        
if __name__ == "__main__":
    # Test block
    test_retrieval("What is the password policy?")
