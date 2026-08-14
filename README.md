# Agentic RAG Framework

## An Agentic Retrieval-Augmented Generation Framework for Multi-Hop Question Answering Using Multi-Agent Collaboration

This repository contains the implementation and experimental artifacts for an **Agentic Retrieval-Augmented Generation (RAG) framework for multi-hop question answering**. The framework decomposes question answering into planning, evidence retrieval, reasoning, and claim-level verification stages coordinated through **LangGraph**.

The proposed system is designed to address limitations of conventional single-pass RAG systems, particularly their inability to reliably decompose multi-hop questions, retrieve evidence iteratively, synthesize evidence across passages, and independently verify generated claims.

The framework was evaluated on a stratified sample of **120 HotpotQA distractor questions**, including bridge and comparison reasoning. The complete system achieved **59.17% Exact Match (EM)** and **68.87% F1**, compared with **30.00% EM** and **35.59% F1** for the baseline RAG configuration.

---

# Key Features

- **Multi-Agent RAG Architecture**: Separates question answering into specialized planning, retrieval, reasoning, and verification agents.
- **Query Decomposition**: The Planner Agent converts a multi-hop question into retrieval-oriented sub-queries.
- **Semantic Evidence Retrieval**: The Evidence Retrieval Agent searches a ChromaDB vector index using dense embeddings.
- **Evidence Ranking**: Retrieved passages are deduplicated and ranked using retrieval similarity and planner confidence.
- **Evidence-Based Reasoning**: The Reasoner Agent synthesizes atomic facts from retrieved evidence before generating the draft answer.
- **Deterministic Claim Verification**: The Verifier Agent independently retrieves evidence for atomic claims in the generated answer.
- **Evidence Sufficiency Score (ESS)**: Measures the proportion of generated claims that are independently supported by retrieved evidence.
- **Iterative Correction**: Unsupported claims are returned to the reasoning stage for correction and regeneration.
- **Citation-Aware Answers**: Supported claims can be accompanied by source-level citations and the corresponding ESS.
- **Pluggable LLM Backend**: The framework is designed to work with different LLM providers and locally hosted models.

---

# Architecture Overview

<p align="center">
  <img src="https://raw.githubusercontent.com/Jish-k/MultiAgent-enterprise-RAG/main/evaluation/paper_assets/figures/architecture.png" width="900">
</p>

The proposed framework consists of four cooperating agents:

1. **Planner Agent**  
   Analyzes the user question and decomposes it into targeted retrieval-oriented sub-queries.

2. **Evidence Retrieval Agent**  
   Performs semantic search over the ChromaDB vector index, removes duplicate evidence, ranks retrieved passages, and constructs an evidence bundle.

3. **Reasoner Agent**  
   Synthesizes atomic facts from the retrieved evidence, performs internal self-critique, and generates a draft response.

4. **Verifier Agent**  
   Extracts atomic claims from the draft, independently retrieves supporting evidence, computes the Evidence Sufficiency Score, and triggers correction when claims are unsupported.

The end-to-end process is:

```text
User Question
      |
      v
Planner Agent
      |
      v
Sub-Query Decomposition
      |
      v
Evidence Retrieval Agent
      |
      v
ChromaDB Vector Index
      |
      v
Evidence Ranking & Deduplication
      |
      v
Reasoner Agent
      |
      v
Draft Answer
      |
      v
Claim Extraction
      |
      v
Verifier Agent
      |
      +---- Unsupported Claims ----> Reasoner Agent
      |
      v
Final Verified Answer
```

---

# Corpus Indexing

The retrieval corpus is constructed from the supporting paragraphs associated with HotpotQA examples.

The indexing pipeline consists of:

```text
HotpotQA Supporting Paragraphs
            |
            v
     Passage Chunking
            |
            v
Sentence-Transformer
   all-MiniLM-L6-v2
            |
            v
       ChromaDB
     Vector Index
```

The experiments use a **1000-character passage size with 200-character overlap** using LangChain's `RecursiveCharacterTextSplitter`.

Each indexed passage stores additional metadata including:

- Document title
- Paragraph number
- Chunk number

This metadata supports traceability between retrieved evidence and the original corpus.

---

# Multi-Agent Processing Pipeline

## 1. Planner Agent

The Planner Agent analyzes the original question and decomposes it into sub-questions corresponding to individual information requirements.

This is particularly important for HotpotQA bridge and comparison questions, where the system may first need to identify an intermediate entity before retrieving the final answer.

---

## 2. Evidence Retrieval Agent

For every planner-generated sub-query, the Retrieval Agent:

- Generates the query embedding
- Retrieves top-k candidate chunks from ChromaDB
- Removes duplicate chunks
- Computes retrieval similarity
- Incorporates planner confidence
- Ranks the evidence
- Selects the highest-ranked evidence set

The ranking score used in the framework is:

```text
S(e) = 0.6 × Sr(e) + 0.4 × Sp(e)
```

where:

- `Sr(e)` = retrieval similarity
- `Sp(e)` = planner confidence

---

## 3. Reasoner Agent

The Reasoner Agent receives the ranked evidence bundle and:

- Synthesizes atomic key facts
- Resolves dependencies across retrieved passages
- Removes redundant information
- Performs an internal self-critique
- Generates the draft answer

The Reasoner is therefore responsible for connecting evidence from different retrieval hops before producing the response.

---

## 4. Verifier Agent

The Verifier Agent performs an independent, claim-level verification stage.

For a generated draft answer:

1. Atomic factual claims are extracted.
2. Each claim is independently checked against the ChromaDB index.
3. Claims are marked as supported or unsupported.
4. The Evidence Sufficiency Score (ESS) is calculated.
5. Unsupported claims are sent back to the reasoning stage.
6. The answer is regenerated using validated evidence.
7. Supporting citations and ESS are attached to the final response.

The Evidence Sufficiency Score is:

```text
ESS = Nsup / Ntotal
```

where:

- `Nsup` = number of independently supported claims
- `Ntotal` = total number of extracted atomic claims

---

# Experimental Dataset

The framework was evaluated on the **HotpotQA** benchmark, a multi-hop question answering dataset containing questions that require combining evidence from multiple supporting paragraphs.

To account for computational and API constraints, the study used a stratified sample of:

- **120 questions**
- HotpotQA **Distractor** setting
- Bridge reasoning questions
- Comparison reasoning questions

### Dataset

**HotpotQA**

https://huggingface.co/datasets/hotpotqa/hotpot_qa

---

# Experimental Configurations

Four configurations were evaluated on the same 120-question test set:

| Configuration | Description |
|---|---|
| **Baseline RAG** | Single-shot retrieval without query decomposition or verification |
| **Stage 1 (Decomp.)** | Adds query decomposition and sub-query retrieval |
| **Stage 2 (Reasoner)** | Adds evidence synthesis and self-critique |
| **Stage 3 (Full)** | Complete system with deterministic claim-level verification |

This staged evaluation isolates the contribution of decomposition, reasoning, and verification.

---

# Performance Evaluation

## Quantitative Results

<p align="center">
  <img src="https://raw.githubusercontent.com/Jish-k/MultiAgent-enterprise-RAG/main/evaluation/paper_assets/figures/HeatMap.png" width="750">
</p>

| Configuration | EM (%) | F1 (%) | Sp F1 (%) | Joint F1 (%) | Latency (s) | ESS |
|---|---:|---:|---:|---:|---:|---:|
| Baseline RAG | 30.00 | 35.59 | 0.00 | 0.00 | 0.39 | – |
| Stage 1 (Decomp.) | 29.17 | 34.76 | 0.00 | 0.00 | 0.93 | – |
| Stage 2 (Reasoner) | 45.00 | 54.51 | 0.00 | 0.00 | 4.43 | – |
| **Stage 3 (Full)** | **59.17** | **68.87** | **13.89** | **9.59** | **36.84*** | **0.82** |

### Main Findings

- The complete Agentic RAG system achieves **59.17% EM** and **68.87% F1**.
- Compared with the baseline RAG system, this represents gains of **29.17 percentage points in EM** and **33.28 percentage points in F1**.
- Query decomposition alone does not improve performance: Stage 1 obtains **29.17% EM** and **34.76% F1**.
- A substantial improvement occurs after introducing evidence synthesis and reasoning in Stage 2.
- The complete Stage 3 system further improves results through deterministic claim-level verification.
- The full system achieves an average **ESS of 0.82**.

> *The reported 36.84 s latency is the mean latency after excluding evaluations affected by internal API retry events. The unfiltered mean latency was 157.87 s because of third-party API rate-limit retries.*

---

# Evidence Verification Results

The Verifier Agent achieved an average **Evidence Sufficiency Score of 0.82** across the 120 evaluated answers.

Verification analysis reported:

- **88/120 answers (73.3%)** achieved full claim support with ESS = 1.0.
- **13/120 answers (10.8%)** received ESS = 0.0 because no independent supporting evidence was found or the system abstained.
- The median ESS was **1.0**.
- The reported standard deviation was **0.33**.

The verifier independently re-searches the vector index for atomic claims rather than relying only on the retrieval context originally used to generate the answer.

---

# Capability Coverage

<p align="center">
  <img src="https://raw.githubusercontent.com/Jish-k/MultiAgent-enterprise-RAG/main/evaluation/paper_assets/figures/capability_comparison_ieee.png" width="850">
</p>

The capability comparison visualization summarizes the coverage of representative RAG and agentic QA approaches across the selected architectural capabilities.

The proposed framework is represented as covering all **7/7** capabilities considered in the comparison.

> **Note:** Capability coverage represents binary architectural coverage and should not be interpreted as empirical performance.

---

# Evaluation Metrics

The framework uses the following evaluation measures:

### Exact Match (EM)

Measures whether the normalized generated answer exactly matches the reference answer.

### F1 Score

Measures token-level overlap between the generated answer and the reference answer.

### Supporting Fact F1 (Sp F1)

Evaluates the quality of the supporting facts identified by the system against the gold supporting-fact set.

### Joint EM/F1

Combines answer correctness with supporting-fact correctness.

### Evidence Sufficiency Score (ESS)

Measures the fraction of generated atomic claims that can be independently supported by retrieved evidence.

---

# Latency Analysis

The agentic pipeline introduces additional latency compared with single-pass RAG because it performs multiple LLM calls and vector-search operations.

The reported configuration-level mean latencies are:

| Configuration | Mean Latency |
|---|---:|
| Baseline RAG | 0.39 s |
| Stage 1 (Decomp.) | 0.93 s |
| Stage 2 (Reasoner) | 4.43 s |
| Stage 3 (Full) | 36.84 s* |

The full system is substantially slower than the baseline because the pipeline includes planning, reasoning, self-critique, answer generation, claim extraction, and independent verification.

The paper reports an unfiltered mean of **157.87 s**, heavily affected by API retry outliers. After excluding evaluations with internal retry events, the mean/median latency is **36.84 s / 37.31 s**.

---

# Qualitative Verification Behavior

The verification stage was designed to identify fluent but unsupported answers.

Two representative failure patterns discussed in the study include:

### 1. Mis-attributed Literary Movement

The Reasoner initially generated an incorrect literary movement for an entity. The Verifier independently searched the corpus, found no supporting evidence for the claim, assigned it an ESS of 0.0, and returned the unsupported claim to the reasoning stage.

### 2. Entity and Answer-Type Mismatch

For a question asking for the title of a film, the initial generation returned the name of an actor instead. Claim-level verification identified that the generated claim was not supported by the evidence and triggered correction.

These cases illustrate the primary purpose of decoupling generation from verification: a fluent answer is not automatically accepted unless its factual claims are supported by evidence.

---

# Pluggable LLM Backend

The Reasoner and Verifier components are designed to remain independent of a single LLM vendor.

The framework supports switching between backend providers or locally hosted models without changing the behavior of the agents.

Potential backends described in the paper include:

- OpenAI
- Anthropic
- Groq
- Ollama / locally hosted models

For the reported experiments, the system uses:

```text
LLM: llama-3.1-8b-instant
Provider: Groq
```

The LLM is used by the Planner, Reasoner, Verifier, and Draft Generator components.

---

# Tech Stack

- **Language:** Python
- **Agent Orchestration:** LangGraph
- **LLM / RAG Framework Components:** LangChain
- **Vector Database:** ChromaDB
- **Embedding Model:** Sentence-Transformer `all-MiniLM-L6-v2`
- **LLM:** Llama-3.1-8B-Instant via Groq
- **Dataset:** HotpotQA
- **Retrieval:** Dense semantic retrieval
- **Evaluation:** EM, F1, Supporting Fact F1, Joint F1, ESS, latency

---

# Installation

Clone the repository:

```bash
git clone https://github.com/Jish-k/MultiAgent-enterprise-RAG.git
cd MultiAgent-enterprise-RAG
```

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

Configure the required LLM/API credentials according to the backend selected for the experiment.

For the reported experiments, the Groq backend was used with the `llama-3.1-8b-instant` model.

---

# Usage

The complete pipeline follows the sequence:

```text
1. Load HotpotQA supporting paragraphs
2. Split passages into chunks
3. Generate dense embeddings
4. Store embeddings in ChromaDB
5. Receive a multi-hop question
6. Decompose the question using the Planner Agent
7. Retrieve evidence for each sub-query
8. Deduplicate and rank evidence
9. Synthesize atomic facts using the Reasoner Agent
10. Generate a draft answer
11. Extract atomic claims
12. Independently retrieve evidence for each claim
13. Calculate ESS
14. Correct unsupported claims when necessary
15. Produce the final verified answer
```

---

# Repository Structure

```text
MultiAgent-enterprise-RAG/
│
├── evaluation/
│   └── paper_assets/
│       └── figures/
│           ├── architecture.png
│           ├── capability_comparison_ieee.png
│           └── HeatMap.png
│
├── notebooks/
│   └── ...
│
├── src/
│   └── ...
│
├── requirements.txt
│
└── README.md
```

> The exact source-code directory structure may vary with the repository version. The figures shown above correspond to the paper and evaluation artifacts used for this README.

---

# Project Statistics

| Component | Value |
|---|---:|
| Dataset | HotpotQA |
| Evaluation Questions | **120** |
| Experimental Configurations | **4** |
| Agents | **4** |
| Vector Database | **ChromaDB** |
| Embedding Model | **all-MiniLM-L6-v2** |
| LLM | **Llama-3.1-8B-Instant (Groq)** |
| Evaluation Metrics | **EM, F1, Sp F1, Joint F1, ESS, Latency** |
| Full-System EM | **59.17%** |
| Full-System F1 | **68.87%** |
| Full-System ESS | **0.82** |

---

# Reproducibility Notes

The reported experiments use the same set of **120 HotpotQA questions** across all four configurations.

The retrieval corpus is constructed from the corresponding supporting paragraphs, with:

- 1000-character chunks
- 200-character overlap
- Sentence-Transformer embeddings
- ChromaDB vector storage

The comparison is therefore intended to measure the incremental contribution of:

```text
Baseline RAG
      ↓
Query Decomposition
      ↓
Reasoning + Self-Critique
      ↓
Claim-Level Verification
```

---

# Limitations

The study identifies several limitations:

- Evaluation is limited to the HotpotQA dataset.
- The framework introduces substantially higher latency than single-pass RAG.
- Performance depends on effective question decomposition.
- Retrieval quality directly affects downstream reasoning and verification.
- The system depends on external LLM/API availability and rate limits.
- Real-world performance across diverse domains has not yet been established.

---

# Future Work

Future development directions include:

- Improving end-to-end execution speed
- Optimizing retrieval quality
- Improving question decomposition
- Strengthening claim-level verification
- Evaluating the framework on diverse datasets
- Exploring the accuracy–reliability–latency trade-off
- Reducing computational and API costs
- Extending evaluation beyond HotpotQA
- Improving robustness under different retrieval and LLM configurations

---

# Citation

If you use this work in your research, please cite:

```bibtex
@article{ka2025agenticrag,
  title={An Agentic Retrieval-Augmented Generation Framework for Multi-Hop Question Answering Using Multi-Agent Collaboration},
  author={Jishnu Ka and Balaji Va and Karthikeyan Pa and Ashwini Kumar Mathura},
  journal={Procedia Computer Science},
  year={2025}
}
```

---

# References

1. Lewis, P., Perez, E., Piktus, A., et al. *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS, 2020.

2. Asai, A., Wu, Z., Wang, Y., Sil, A., and Hajishirzi, H. *Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection*. ICLR, 2024.

3. Karpukhin, V., Oguz, B., Min, S., et al. *Dense Passage Retrieval for Open-Domain Question Answering*. EMNLP, 2020.

4. Gao, L., Ma, X., Lin, J., and Callan, J. *Precise Zero-Shot Dense Retrieval without Relevance Labels*. ACL, 2023.

5. Wei, J., Wang, X., Schuurmans, D., et al. *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. NeurIPS, 2022.

6. Yao, S., Zhao, J., Yu, D., et al. *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR, 2023.

7. Wu, Q., Bansal, G., Zhang, J., et al. *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*. arXiv, 2023.

8. Yan, S.-Q., Gu, J.-C., Zhu, Y., and Ling, Z.-H. *Corrective Retrieval Augmented Generation*. arXiv, 2024.

9. Jeong, S., Baek, J., Cho, S., Hwang, S. J., and Park, J. C. *Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity*. NAACL, 2024.

10. Jiang, Z., Xu, F. F., Gao, L., et al. *Active Retrieval Augmented Generation*. EMNLP, 2023.

11. Trivedi, H., Balasubramanian, N., Khot, T., and Sabharwal, A. *Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions*. ACL, 2023.

12. Sarthi, P., Abdullah, S., Tuli, A., et al. *RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval*. ICLR, 2024.

13. Edge, D., Trinh, H., Cheng, N., et al. *From Local to Global: A GraphRAG Approach to Query-Focused Summarization*. arXiv, 2024.

---

# Source Code and Data Availability

The implementation associated with the study is available at:

https://github.com/Jish-k/MultiAgent-enterprise-RAG

The HotpotQA dataset is publicly available at:

https://huggingface.co/datasets/hotpotqa/hotpot_qa

The framework and evaluation results described in this README are based on the accompanying research paper:

**An Agentic Retrieval-Augmented Generation Framework for Multi-Hop Question Answering Using Multi-Agent Collaboration**

