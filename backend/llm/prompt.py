from langchain_core.prompts import ChatPromptTemplate

# A standard RAG Prompt
# Strictly enforces the AI to only use the provided context.
RAG_SYSTEM_PROMPT = """You are a highly precise AI Assistant.
Your job is to answer questions accurately based strictly on the provided documents.

Use the following pieces of retrieved context to answer the question. 
If the answer is not contained within the context, simply say "I don't know". Do not make up information.

Context:
{context}

CRITICAL: Output ONLY the exact entity, short phrase, or short answer. Do not write full sentences. Do not use conversational filler (e.g. "The answer is...")."""

def get_rag_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", RAG_SYSTEM_PROMPT),
        ("human", "{question}")
    ])
