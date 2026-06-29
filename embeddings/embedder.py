from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings

@lru_cache(maxsize=1)
def get_embedding_model(model_name="all-MiniLM-L6-v2"):
    """
    Initializes and returns the HuggingFace embedding model.
    Downloads the model locally if not already cached.
    """
    print(f"Loading embedding model: {model_name}...")
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return embeddings
