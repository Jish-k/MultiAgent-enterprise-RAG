import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # LLM Settings
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama") # "ollama", "groq", or "openai"
    
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
    
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.0"))
    
    # Retrieval Settings
    RETRIEVER_K = int(os.getenv("RETRIEVER_K", "3"))
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CHROMA_PERSIST_DIR = os.path.join(BASE_DIR, "embeddings", "chroma_db")
