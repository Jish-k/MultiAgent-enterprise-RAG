import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from llm.provider import get_llm
from llm.prompt import get_rag_prompt
from rag.retriever import get_rag_retriever, format_docs

def build_rag_chain():
    """
    Builds the LCEL (LangChain Expression Language) chain for the Baseline RAG.
    Flow: User Question -> Retriever -> Context Formatting -> Prompt -> LLM -> String Output
    """
    retriever = get_rag_retriever()
    llm = get_llm()
    prompt = get_rag_prompt()
    
    # Define the core RAG logic using LCEL
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain
