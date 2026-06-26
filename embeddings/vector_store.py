import os
from langchain_chroma import Chroma
from .embedder import get_embedding_model

CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

def get_vector_store(embedding_model=None):
    """
    Initializes and returns the Chroma vector database.
    """
    if embedding_model is None:
        embedding_model = get_embedding_model()
        
    vector_store = Chroma(
        collection_name="enterprise_hr_docs",
        embedding_function=embedding_model,
        persist_directory=CHROMA_PERSIST_DIR
    )
    return vector_store

def add_to_vector_store(documents, vector_store=None):
    """
    Embeds and stores document chunks into the Chroma database.
    """
    if not documents:
        print("No documents to add.")
        return
        
    if vector_store is None:
        vector_store = get_vector_store()
        
    print(f"Adding {len(documents)} chunks to ChromaDB...")
    vector_store.add_documents(documents)
    print("Successfully added chunks to vector store.")
    return vector_store
