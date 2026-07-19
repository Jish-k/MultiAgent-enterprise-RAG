import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from agents.reasoner.analyzer import EvidenceAnalyzer
from agents.reasoner.generator import DraftGenerator
from agents.reasoner.models import ReasoningOutput, ReasoningAnalysis, ReasonerMetrics
from agents.retriever.models import EvidencePackage

class ReasonerAgent:
    """
    Agent 3: The Reasoner Agent (Evidence Analyst)
    Transforms raw retrieved chunks into a synthesized, grounded response.
    """
    
    def __init__(self):
        self.analyzer = EvidenceAnalyzer()
        self.generator = DraftGenerator()
        
    def reason(self, question: str, evidence_package: EvidencePackage) -> ReasoningOutput:
        metrics = ReasonerMetrics()
        
        # Phase A: Analyze & Synthesize
        start_time = time.time()
        analysis_data = self.analyzer.analyze(question, evidence_package)
        metrics.analysis_time_ms = (time.time() - start_time) * 1000
        
        # Calculate Evidence Utilization Rate
        total_chunks = len(evidence_package.chunks)
        
        # Ensure fallback data fits the schema if LLM hallucinated the JSON keys
        used = analysis_data.get("used_chunks", [])
        discarded = analysis_data.get("discarded_chunks", [])
        facts = analysis_data.get("key_facts", [])
        conflicts = analysis_data.get("conflicts", [])
        missing = analysis_data.get("missing_information", [])
        
        if total_chunks > 0:
            metrics.evidence_utilization_rate = (len(used) / total_chunks) * 100
            
        analysis_obj = ReasoningAnalysis(
            key_facts=facts,
            used_chunks=used,
            discarded_chunks=discarded,
            conflicts=conflicts,
            missing_information=missing
        )
        
        # Phase B: Draft Generation
        start_time = time.time()
        draft_text = self.generator.generate(question, analysis_obj.key_facts)
        metrics.generation_time_ms = (time.time() - start_time) * 1000
        
        metrics.total_time_ms = metrics.analysis_time_ms + metrics.generation_time_ms
        
        # Parse the structured draft text
        parts = draft_text.split("[Evidence Summary]")
        answer_part = parts[0].replace("[Grounded Answer]", "").strip()
        summary_part = parts[1].strip() if len(parts) > 1 else ""
        
        return ReasoningOutput(
            answer=answer_part,
            evidence_summary=summary_part,
            analysis=analysis_obj,
            metrics=metrics
        )
