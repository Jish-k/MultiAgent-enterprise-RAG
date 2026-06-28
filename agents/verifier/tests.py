import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from agents.verifier.agent import VerifierAgent
from agents.retriever.models import RankedChunk
from agents.reasoner.models import ReasoningOutput

def test_verifier():
    print("Initializing Verifier Agent...")
    agent = VerifierAgent(threshold=0.50) # low threshold for test
    
    draft_answer = "Employees receive 26 weeks of paid maternity leave. The HR Head must approve it."
    
    mock_chunks = [
        RankedChunk(
            chunk_id="chunk_1",
            content="Female employees are entitled to 26 weeks of paid maternity leave.",
            document="Leave_Policy.pdf",
            page=7,
            section="Maternity Leave",
            metadata={},
            retrieval_similarity=0.9,
            final_score=0.9
        ),
        RankedChunk(
            chunk_id="chunk_2",
            content="Maternity leave applications must be approved by the Department Head, not HR.",
            document="Leave_Policy.pdf",
            page=8,
            section="Maternity Leave Approval",
            metadata={},
            retrieval_similarity=0.85,
            final_score=0.85
        )
    ]
    
    required_info = ["maternity leave", "approval authority"]
    
    print("\nDraft Answer:", draft_answer)
    print("Required Info:", required_info)
    print("\nRunning Verification...")
    
    result = agent.verify(
        draft_answer=draft_answer,
        used_chunks=mock_chunks,
        required_information=required_info
    )
    
    print("\n=== VERIFICATION RESULTS ===")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"ESS: {result.verification_metrics.evidence_sufficiency_score:.2f}")
    print("\nExtracted Claims:")
    for c in result.claims:
        print(f" - {c}")
        
    print("\nSupported Claims:")
    for sc in result.supported_claims:
        print(f" - [Sim: {sc.similarity_score:.2f}] {sc.claim} (Source: {sc.chunk_id})")
        
    print("\nUnsupported Claims (Hallucinations?):")
    for uc in result.unsupported_claims:
        print(f" - {uc}")
        
    print("\nCitations:")
    for c in result.citations:
        print(f" - {c}")

if __name__ == "__main__":
    test_verifier()
