# Threats to Validity

This document transparently outlines the limitations and validity threats of our experimental methodology, ensuring that our claims remain scoped appropriately for the final paper.

## 1. Internal Validity
*Are the observed effects truly caused by the architectural changes (Planner, Reasoner, Verifier), or could they be attributed to experimental artifacts?*

- **Configuration Parity:** All four configurations (A, B, C, D) were run using identical model parameters (e.g., `llama-3.1-8b`, `temperature=0.0`), the same embedding model (`all-MiniLM-L6-v2`), and identical chunking parameters (`chunk_size=500, chunk_overlap=50`).
- **Prompt Isolation:** Prompts were strictly frozen via an `experiment_manifest.json` before execution. Any variation in performance is explicitly tied to the addition of an agentic node, not an undocumented prompt tweak.
- **Code Stability:** The evaluation pipeline code is version-locked to a specific git commit (`v1.0-pilot-validated`), preventing mid-benchmark bug fixes from skewing comparative metrics.

## 2. Construct Validity
*Do our evaluation metrics accurately measure the theoretical constructs we are claiming to improve?*

- **Composite Score Dependency:** Our primary "Final Accuracy" relies on a 40% rule-based (Exact Match, Semantic Similarity) and 60% LLM-Judge split. While pragmatic, LLM-as-a-judge inherently introduces a black-box variance. We mitigate this by reporting the distinct rule-based metrics alongside the composite score.
- **Evidence Sufficiency (ESS):** ESS relies on an LLM to evaluate if the retrieved context contains the answer. While calibrated, it is not an absolute mathematical proof of context completeness.
- **Hallucination Rate:** Measured via citation accuracy and direct LLM inspection, which may occasionally penalize implicitly true but uncited facts.

## 3. External Validity
*How well do these findings generalize outside of this specific experimental setup?*

- **Synthetic Enterprise Corpus:** The benchmark utilizes a synthetically generated set of enterprise policy documents. Results may differ when applied to highly unstructured, messy, or massive-scale production knowledge bases.
- **Model Specificity:** Experiments were conducted exclusively using Groq's `llama-3.1-8b`. The observed benefits of the Reasoner or Verifier may diminish or amplify when using significantly larger (e.g., GPT-4) or smaller parameter models.
- **Embedding Dependency:** Performance heavily depends on `all-MiniLM-L6-v2`. A more sophisticated embedding model could potentially raise the baseline (Config A) accuracy, thereby reducing the marginal utility of the Planner.

## 4. Conclusion Validity
*Are our conclusions statistically sound and logically derived from the evidence?*

- **Sample Size:** The full benchmark consists of 140 stratified questions. While sufficient for broad conclusions, specific category subsets (e.g., 'Adversarial' with 20 questions) may lack the statistical power for highly granular claims.
- **Variance and Noise:** We execute 3 runs per configuration to capture variance. We commit to explicitly reporting standard deviations and rejecting any claims where the margin of improvement overlaps with the statistical noise (e.g., claiming victory over a +0.4% delta).
- **Negative Results Reporting:** If an ablation fails to show improvement (e.g., the Verifier only increases latency without improving accuracy), it will be fully documented as a limitation of the current architecture.
