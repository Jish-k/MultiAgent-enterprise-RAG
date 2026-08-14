# Benchmark Success Criteria

Before executing the Pilot Benchmark or Full Evaluation, the pipeline must meet the following performance expectations:

| Metric | Target Value | Rationale |
|---|---|---|
| Dataset Validation | 100% | All questions, ground truth answers, planner states, and metadata must pass `validate_dataset.py` with no formatting errors or missing fields. |
| Pilot Completion | No runtime failures | The 20-question pilot test must run perfectly for all 4 configurations across 3 runs without crashing Groq's TPM limits. |
| Exact Match | ≥ 85% | Rule-based exact matches should capture core factual retention. |
| Semantic Similarity | ≥ 90% | The generated answers must semantically align closely with human-verified ground truths. |
| Citation Accuracy | ≥ 95% | When the agent uses chunks for reasoning, it must properly map those chunks to citations. |
| ESS (Evidence Sufficiency Score) | ≥ 0.90 | The chunks provided to the LLM must consistently contain the complete answer. |
| Average Confidence | ≥ 0.85 | The Verifier agent must rate the finalized answers as highly confident. |
| Latency | < 3 seconds | Excluding external API variability, the orchestration logic should add minimal overhead. |
