import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

def get_llm(api_key: str = None, anthropic_api_key: str = None, llm_provider: str = None):
    """
    Initializes and returns the language model based on the configuration.
    """
    provider = (llm_provider or Config.LLM_PROVIDER).lower()
    
    if provider == "ollama":
        from langchain_community.chat_models import ChatOllama
        print(f"Initializing local Ollama LLM: {Config.OLLAMA_MODEL}")
        return ChatOllama(
            model=Config.OLLAMA_MODEL,
            temperature=Config.TEMPERATURE
        )
        
    elif provider == "groq":
        from langchain_groq import ChatGroq
        final_api_key = api_key or Config.GROQ_API_KEY
        if not final_api_key or final_api_key == "your_groq_api_key_here":
            raise ValueError("GROQ_API_KEY is missing or invalid in the .env file.")
            
        print(f"Initializing Groq LLM: {Config.GROQ_MODEL}")
        return ChatGroq(
            model_name=Config.GROQ_MODEL,
            temperature=Config.TEMPERATURE,
            groq_api_key=final_api_key,
            max_retries=10,
            timeout=60.0
        )
        
    elif provider == "openai":
        from langchain_openai import ChatOpenAI
        final_api_key = api_key or Config.OPENAI_API_KEY
        if not final_api_key or final_api_key == "your_openai_api_key_here":
            raise ValueError("OPENAI_API_KEY is missing or invalid in the .env file.")
            
        print(f"Initializing OpenAI LLM: {Config.OPENAI_MODEL}")
        return ChatOpenAI(
            model=Config.OPENAI_MODEL,
            temperature=Config.TEMPERATURE,
            openai_api_key=final_api_key,
            max_retries=10,
            timeout=60.0
        )
        
    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        final_api_key = anthropic_api_key or getattr(Config, "ANTHROPIC_API_KEY", None)
        if not final_api_key or final_api_key == "your_anthropic_api_key_here":
            raise ValueError("ANTHROPIC_API_KEY is missing or invalid.")
            
        print(f"Initializing Anthropic LLM: claude-3-haiku-20240307")
        return ChatAnthropic(
            model="claude-3-haiku-20240307",
            temperature=Config.TEMPERATURE,
            api_key=final_api_key
        )
        
    else:
        raise ValueError(f"Unsupported LLM provider: {Config.LLM_PROVIDER}")
