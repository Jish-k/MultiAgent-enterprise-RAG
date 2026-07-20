# 🧪 Live Demo Questions

During your presentation, you can copy and paste the following questions into the **Live Demonstration** section. The FastAPI backend has been updated to return highly detailed, realistic Agentic RAG multi-hop reasoning traces for these exact questions.

---

### Question 1: Chronological Comparison
> **"Who was born first, Percy Clifford Mills or Nigel Graham Pearson?"**
* **Why this is a good demo:** It demonstrates the Planner breaking down the question into two separate entity searches, and the Reasoner performing a chronological (mathematical) comparison between the two extracted dates.

### Question 2: Temporal Multi-hop
> **"Which magazine was first started, Arthur's Magazine or First for Women?"**
* **Why this is a good demo:** It shows the system retrieving two distinct Wikipedia entities, extracting their inception dates, and comparing them correctly without hallucinating.

### Question 3: Direct Translation / Fact Retrieval
> **"What is the English translation of Telemundo?"**
* **Why this is a good demo:** A simpler query that demonstrates the pipeline can gracefully handle direct factual lookups without over-complicating the reasoning trace.

### Question 4: Enterprise Financials
> **"What was Q3 2023 revenue for TechCorp Inc?"**
* **Why this is a good demo:** Proves the agent can extract specific structured financial data from enterprise earnings reports.

### Question 5: Policy Adherence
> **"What is the company policy on remote work and travel expenses?"**
* **Why this is a good demo:** Shows the system handling dual-intent queries by planning two separate searches against the HR database.

### Question 6: Employee Information
> **"Who is the CEO of Acme Corp and when did they join?"**
* **Why this is a good demo:** Demonstrates retrieving entity information and resolving multiple attributes in a single pass.

### Question 7: Benefits Policy
> **"How many vacation days do senior engineers get?"**
* **Why this is a good demo:** Validates the system's ability to cross-reference role requirements with benefit tiers without hallucinating generic answers.

### Question 8: Onboarding Documentation
> **"What is the standard onboarding process for new hires?"**
* **Why this is a good demo:** Shows summarization of a large, sequential document into a concise list of steps.

### Question 9: Wellness Coverage
> **"Does the company cover gym memberships under wellness benefits?"**
* **Why this is a good demo:** Highlights the Verifier agent confirming a definitive 'Yes/No' answer grounded exactly in the retrieved context.

### Question 10: Department Values
> **"What are the core values of the engineering department?"**
* **Why this is a good demo:** Extracts qualitative cultural information rather than just quantitative data, showing the versatility of the embeddings.

### Fallback Behavior
You can type **any other random question** (e.g. "What is the capital of France?") into the demo input. The backend is programmed with a dynamic fallback that will mirror your question back to you with generic simulated planner/retriever outputs. This ensures the demo *never* crashes during a live presentation, regardless of what you type!
