# Claims Traceability Matrix

This document maps every claim intended for the research paper to the exact experimental evidence that supports it.

| Paper Claim | Supporting Evidence (Artifact/Table/Graph) | Status / Notes |
| :--- | :--- | :--- |
| **Planner improves multi-document retrieval** | "Accuracy vs Retrieval Difficulty" Graph + Per-Category Performance Table (specifically the 'Cross Document' row). | *Pending Pilot Results* |
| **Reasoner reduces context size without accuracy loss** | "Context Compression" Graph + "Agent Contribution Matrix" (Context Tokens row). | *Pending Pilot Results* |
| **Verifier improves grounding & hallucination resistance** | "Agent Contribution Matrix" (Citation Accuracy, Hallucination Rate, ESS rows). | *Pending Pilot Results* |
| **Verifier confidence is meaningful / calibrated** | "Confidence Calibration Table" (showing monotonic relationship between score and empirical accuracy). | *Pending Pilot Results* |
| **Full Agentic pipeline outperforms standard RAG baseline** | "Configuration Comparison Table" (Config C vs Config A across exact match, semantic similarity, etc.). | *Pending Pilot Results* |
| **System maintains reasonable end-to-end latency** | "Latency Distribution" Table (Mean, Median, Max). | *Pending Pilot Results* |

## How to use this document
If a reviewer asks for proof of any claim, trace it to the **Evidence** column. The evidence files (PNGs, CSVs) are permanently stored in the `paper/evidence/` and `paper/figures/` directories, completely disconnected from future code changes.
