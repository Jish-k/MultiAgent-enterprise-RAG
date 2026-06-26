import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

def get_llm():
    """
    Initializes and returns the language model based on the configuration.
    """
    if Config.LLM_PROVIDER.lower() == "openai":
        from langchain_openai import ChatOpenAI
        
        if not Config.OPENAI_API_KEY or Config.OPENAI_API_KEY == "your_openai_api_key_here":
            raise ValueError("OPENAI_API_KEY is missing or invalid in the .env file.")
            
        print(f"Initializing OpenAI LLM: {Config.OPENAI_MODEL}")
        return ChatOpenAI(
            model=Config.OPENAI_MODEL,
            temperature=Config.TEMPERATURE,
            openai_api_key=Config.OPENAI_API_KEY
        )
        
    elif Config.LLM_PROVIDER.lower() == "ollama":
        from langchain_community.chat_models import ChatOllama
        
        print(f"Initializing local Ollama LLM: {Config.OLLAMA_MODEL}")
        return ChatOllama(
            model=Config.OLLAMA_MODEL,
            temperature=Config.TEMPERATURE
        )
        
    else:
        raise ValueError(f"Unsupported LLM provider: {Config.LLM_PROVIDER}")
