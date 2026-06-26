import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from llm.provider import get_llm
from agents.reasoner.prompt import get_generation_prompt

class DraftGenerator:
    def __init__(self):
        self.llm = get_llm()
        self.prompt = get_generation_prompt()
        self.chain = self.prompt | self.llm
        
    def generate(self, question: str, key_facts: list[str]) -> str:
        """
        Stage B: Generates the final drafted response using only the synthesized Key Facts.
        """
        if not key_facts:
            return "[Grounded Answer]\nI could not find enough relevant information in the provided documents to answer your question.\n\n[Evidence Summary]\nNone."
            
        facts_text = "\n".join([f"- {fact}" for fact in key_facts])
        
        try:
            response = self.chain.invoke({
                "question": question,
                "key_facts": facts_text
            })
            return response.content.strip()
        except Exception as e:
            print(f"[DraftGenerator Error] {e}")
            return f"[Grounded Answer]\nAn error occurred while generating the answer.\n\n[Evidence Summary]\nError: {e}"
