import os
import sys
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from llm.provider import get_llm
from rag.retriever import get_rag_retriever

PLANNER_PROMPT = """You are an AI planner. Your job is to break down a complex question into simpler, specific search queries that can be used to retrieve information from a database.
Generate 1 to 3 search queries that will help find the information needed to answer the question.
If the question is simple, just output the main entities to search for.
If the question is multi-hop (e.g., "Who was born first, X or Y?"), generate separate queries for X and Y.
Do not output anything other than the search queries, one per line.

Question: {question}
Search Queries:"""

def build_planner_chain():
    llm = get_llm()
    prompt = PromptTemplate.from_template(PLANNER_PROMPT)
    return prompt | llm | StrOutputParser()

def multi_query_retrieve(question: str):
    """
    Runs the planner to generate sub-queries, then retrieves and deduplicates documents for all queries.
    """
    planner_chain = build_planner_chain()
    retriever = get_rag_retriever()
    
    # 1. Generate queries
    queries_text = planner_chain.invoke({"question": question})
    
    # Clean and split queries
    queries = [q.strip() for q in queries_text.split('\n') if q.strip()]
    
    # Always include the original question as well
    if question not in queries:
        queries.insert(0, question)
        
    print(f"   [Planner] Generated {len(queries)} queries: {queries}")
    
    # 2. Retrieve for all queries
    all_docs = []
    seen_sources = set()
    
    for q in queries:
        docs = retriever.invoke(q)
        for doc in docs:
            # Deduplicate by source title to avoid duplicate context
            source = doc.metadata.get("source", "")
            if source not in seen_sources:
                seen_sources.add(source)
                all_docs.append(doc)
                
    return all_docs

def get_planner_retriever():
    """
    Returns a Runnable that takes a question (str) and returns a list of Document objects.
    """
    return RunnableLambda(multi_query_retrieve)
