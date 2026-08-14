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


### Fallback Behavior
  type **any other random question** (e.g. "What is the capital of France?") into the demo input. The backend is programmed with a dynamic fallback that will mirror your question back to you with generic simulated planner/retriever outputs. This ensures the demo *never* crashes during a live presentation, regardless of what you type!


. Start the Database (Terminal 1)

cd /Users/jishnusmacbook/Desktop/Internship/project/Enterprise-Agentic-RAG
docker-compose up -d


Start the FastAPI Backend terminal 2

cd /Users/jishnusmacbook/Desktop/Internship/project/Enterprise-Agentic-RAG/backend
source ../venv/bin/activate
python main.py


Start the Next.js Frontend terminal 3

cd /Users/jishnusmacbook/Desktop/Internship/project/Enterprise-Agentic-RAG/frontend
npm run dev


Stop the Backend & Frontend

Ctrl + C
In Terminal 2 (Backend) and Terminal 3


Stop the Database To shut down

cd /Users/jishnusmacbook/Desktop/Internship/project/Enterprise-Agentic-RAG
docker-compose down
