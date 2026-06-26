import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from agents.reasoner.agent import ReasonerAgent
from agents.retriever.models import EvidencePackage, RankedChunk

def test_reasoner():
    print("Initializing Reasoner Agent...")
    agent = ReasonerAgent()
    
    question = "How many casual leaves am I entitled to, and who approves them?"
    
    mock_chunks = [
        RankedChunk(
            chunk_id="chunk_1",
            content="Employees are entitled to 12 casual leaves per year.",
            document="Leave_Policy.pdf",
            page=2,
            metadata={},
            retrieval_similarity=0.9,
            final_score=0.9
        ),
        RankedChunk(
            chunk_id="chunk_2",
            content="All casual leaves must be approved by the reporting manager.",
            document="Leave_Policy.pdf",
            page=3,
            metadata={},
            retrieval_similarity=0.85,
            final_score=0.85
        ),
        RankedChunk(
            chunk_id="chunk_3",
            content="The cafeteria serves lunch from 1 PM to 2 PM.",
            document="Employee_Handbook.pdf",
            page=15,
            metadata={},
            retrieval_similarity=0.4,
            final_score=0.4
        )
    ]
    
    package = EvidencePackage(request_id="req_test", chunks=mock_chunks, sources=["Leave_Policy.pdf", "Employee_Handbook.pdf"])
    
    print("\nExecuting Reasoning Pipeline (Analyze + Synthesize + Generate)...")
    output = agent.reason(question, package)
    
    print("\n=== Phase A: Analysis ===")
    print(f"Key Facts Extracted: {output.analysis.key_facts}")
    print(f"Used Chunks: {output.analysis.used_chunks}")
    print(f"Discarded Chunks: {output.analysis.discarded_chunks}")
    
    print("\n=== Phase B: Generation ===")
    print(f"Grounded Answer:\n{output.answer}")
    print(f"\nEvidence Summary:\n{output.evidence_summary}")
    
    print("\n=== Reasoner Metrics ===")
    print(f"Evidence Utilization Rate: {output.metrics.evidence_utilization_rate:.1f}%")
    print(f"Analysis Latency: {output.metrics.analysis_time_ms:.1f}ms")
    print(f"Generation Latency: {output.metrics.generation_time_ms:.1f}ms")

if __name__ == "__main__":
    test_reasoner()
