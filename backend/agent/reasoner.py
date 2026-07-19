import os
import sys
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from llm.provider import get_llm

REASONER_PROMPT = """You are an expert AI Reasoner.
You are given a complex multi-hop question and several retrieved context documents.
Your task is to read the context and output a step-by-step logical reasoning trace (Chain of Thought) that leads to the correct answer.

Do not output the final answer alone. Explicitly state the intermediate facts you found.

Context:
{context}

Question: {question}

Step-by-step Reasoning:"""

def build_reasoner_chain():
    llm = get_llm()
    prompt = PromptTemplate.from_template(REASONER_PROMPT)
    return prompt | llm | StrOutputParser()

def build_reasoner_generator_prompt():
    prompt_str = """You are an expert Question Answering system.
Use the provided Context and the Step-by-Step Reasoning trace to answer the final Question.
Keep your answer as concise as possible (e.g., just the entity name, date, or a very short phrase).

Context:
{context}

Reasoning Trace:
{reasoning}

Question: {question}
Final Answer:"""
    return PromptTemplate.from_template(prompt_str)
