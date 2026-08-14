import sys
with open('backend/evaluation/scripts/run_agentic_stage3.py', 'r') as f:
    content = f.read()

# Add import
content = content.replace(
    "from agent.verifier import build_verifier_chain",
    "from agent.verifier import build_verifier_chain\nfrom verifier.agent import VerifierAgent"
)

# Instantiate
content = content.replace(
    "verifier_chain = build_verifier_chain()",
    "verifier_chain = build_verifier_chain()\n    verifier_agent = VerifierAgent(threshold=0.50)"
)

# Add logic after prediction
new_logic = """
            prediction = generator_chain.invoke({
                "context": context_str,
                "reasoning": verified_reasoning,
                "question": question
            })
            
            # Evaluate with VerifierAgent to get ESS
            v_resp = verifier_agent.verify(prediction, retrieved_docs, [])
            ess = v_resp.verification_metrics.evidence_sufficiency_score
            citations = [c.source for c in v_resp.citations] if v_resp.citations else []
            citations_str = "|".join(citations)
"""
content = content.replace(
    """            prediction = generator_chain.invoke({
                "context": context_str,
                "reasoning": verified_reasoning,
                "question": question
            })""",
    new_logic
)

# Add to result_row
content = content.replace(
    '"prediction": prediction.replace(\'\\n\', \' \'),',
    '"prediction": prediction.replace(\'\\n\', \' \'),\n            "ess": ess,\n            "citations": citations_str,'
)

with open('backend/evaluation/scripts/run_agentic_stage3.py', 'w') as f:
    f.write(content)
