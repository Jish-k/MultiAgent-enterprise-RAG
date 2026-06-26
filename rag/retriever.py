import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from embeddings.retrieval import get_retriever as get_vector_retriever
from config import Config

def format_docs(docs):
    """
    Formats the retrieved LangChain Document objects into a single context string.
    Includes metadata like source and page number to help the LLM cite its sources.
    """
    formatted_context = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "Unknown Document")
        page = doc.metadata.get("page_number", "?")
        section = doc.metadata.get("section", "Unknown Section")
        content = doc.page_content
        
        formatted_context.append(f"--- Document {i} ({source}, Page {page}, {section}) ---\n{content}\n")
        
    return "\n".join(formatted_context)

def get_rag_retriever():
    """
    Returns the vector database retriever.
    """
    return get_vector_retriever(k=Config.RETRIEVER_K)
