import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from llm.provider import get_llm
from agents.reasoner.prompt import get_analysis_prompt
from agents.retriever.models import EvidencePackage

class EvidenceAnalyzer:
    def __init__(self):
        # We explicitly set model kwargs to ensure JSON mode on supported models like Groq, 
        # though standard prompt constraints usually suffice for local Llama3
        self.llm = get_llm() 
        self.prompt = get_analysis_prompt()
        self.chain = self.prompt | self.llm
        
    def analyze(self, question: str, evidence_package: EvidencePackage) -> dict:
        """
        Stage A: Analyzes and synthesizes the evidence into key facts.
        """
        evidence_text = ""
        for chunk in evidence_package.chunks:
            evidence_text += f"--- Chunk ID: {chunk.chunk_id} ---\nSource: {chunk.document} (Page {chunk.page})\nContent: {chunk.content}\n\n"
            
        try:
            response = self.chain.invoke({
                "question": question,
                "evidence": evidence_text
            })
            
            raw_content = response.content.strip()
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:-3].strip()
            elif raw_content.startswith("```"):
                raw_content = raw_content[3:-3].strip()
                
            return json.loads(raw_content)
            
        except Exception as e:
            print(f"[EvidenceAnalyzer Error] {e}")
            return {
                "key_facts": [],
                "used_chunks": [],
                "discarded_chunks": [c.chunk_id for c in evidence_package.chunks],
                "conflicts": [],
                "missing_information": ["Failed to extract facts."]
            }
