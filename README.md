# Agentic RAG Framework for Enterprise Knowledge Management

This repository contains a prototype for an Enterprise AI Assistant using a Multi-Agent Retrieval-Augmented Generation (RAG) framework. The system is designed to read enterprise documents, answer user questions, use multiple collaborating AI agents to verify answers, provide citations, and minimize hallucinations.

## Key Features
- **Traditional RAG Baseline**: A standard linear pipeline for benchmark comparison.
- **Agentic RAG Framework**: A multi-agent collaborative system (Router, Retriever, Synthesizer, Verifier).
- **Fact-Checking Agent**: Actively verifies generated answers against retrieved context to reduce hallucinations.

## Architecture
The system uses LangGraph to coordinate the following agents:
1. **Router Agent**: Directs queries to the appropriate tools or databases.
2. **Retriever Agent**: Optimizes search and retrieves relevant context from ChromaDB.
3. **Synthesizer Agent**: Drafts responses with explicit citations.
4. **Verifier Agent**: Critiques and fact-checks the draft against the source context before returning it to the user.

## Tech Stack
- **Language**: Python
- **Framework**: LangChain, LangGraph
- **Vector DB**: ChromaDB
- **LLM APIs**: Gemini / OpenAI (configurable)
- **UI**: Streamlit (planned)
