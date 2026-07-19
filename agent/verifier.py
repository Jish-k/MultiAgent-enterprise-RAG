import os
import sys
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from llm.provider import get_llm

VERIFIER_PROMPT = """You are an expert AI Verifier.
You are given a complex multi-hop question, retrieved context documents, and an initial Step-by-Step Reasoning trace.
Your task is to review the reasoning trace against the context to catch any logical fallacies, hallucinated facts, or incorrect conclusions.
If the reasoning trace is correct, refine it to be as accurate as possible.
If it is incorrect, output a fully corrected step-by-step reasoning trace based on the context.

Context:
{context}

Question: {question}

Initial Reasoning Trace:
{reasoning}

Verified Step-by-Step Reasoning Trace:"""

def build_verifier_chain():
    llm = get_llm()
    prompt = PromptTemplate.from_template(VERIFIER_PROMPT)
    return prompt | llm | StrOutputParser()
