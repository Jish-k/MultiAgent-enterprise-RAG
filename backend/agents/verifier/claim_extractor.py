import sys
import os
import json
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from llm.provider import get_llm
from langchain_core.prompts import ChatPromptTemplate

EXTRACTOR_SYSTEM_PROMPT = """You are an expert Claim Extractor.
Your job is to read a draft answer and decompose it into a list of singular, atomic claims.
Each claim should contain one specific fact.

You must output ONLY valid JSON matching this schema:
{{
  "claims": [
    "Atomic claim 1.",
    "Atomic claim 2."
  ]
}}

Draft Answer:
{draft_answer}
"""

class ClaimExtractor:
    """
    Module 1: LLM-based Claim Extractor.
    Extracts atomic factual claims from the Draft Answer.
    """
    def __init__(self):
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_messages([("system", EXTRACTOR_SYSTEM_PROMPT)])
        self.chain = self.prompt | self.llm
        
    def extract(self, draft_answer: str) -> list[str]:
        try:
            response = self.chain.invoke({"draft_answer": draft_answer})
            content = response.content.strip()
            
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
                return data.get("claims", [])
            return []
        except Exception as e:
            print(f"[ClaimExtractor Error] {e}")
            return []
