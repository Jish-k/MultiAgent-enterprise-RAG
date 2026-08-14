# Agentic RAG Framework

This repository contains a prototype for an AI Assistant using a Multi-Agent Retrieval-Augmented Generation (RAG) framework evaluated on the HotpotQA benchmark. The system is designed to read documents, answer user questions, use multiple collaborating AI agents to verify answers, provide citations, and minimize hallucinations.

## Key Features
- **Traditional RAG Baseline**: A standard linear pipeline for benchmark comparison.
- **Agentic RAG Framework**: A multi-agent collaborative system (Router, Retriever, Synthesizer, Verifier).
- **Fact-Checking Agent**: Actively verifies generated answers against retrieved context to reduce hallucinations.

## Architecture
The system uses LangGraph to coordinate the following agents:

<p align="center">
  <img src="evaluation/paper_assets/figures/architecture.png" width="850">
</p>

## Tech Stack
- **Language**: Python
- **Framework**: LangChain, LangGraph
- **Vector DB**: ChromaDB
- **LLM APIs**: Gemini / OpenAI (configurable)
- **UI**: Streamlit (planned)

## Project Statistics
- **Documents**: 6
- **Chunks**: 162
- **Questions**: 140
- **Gold Standard**: 25
- **Agents**: 4
- **Benchmark Configurations**: 4
- **Evaluation Metrics**: 10+
- **Ablation Experiments**: 4
- **Graphs Generated**: 8+
- **Vector Database**: ChromaDB
- **Embedding Model**: all-MiniLM-L6-v2
- **LLM**: Llama-3.1-8B (Groq)
