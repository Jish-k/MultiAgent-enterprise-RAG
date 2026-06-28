import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from langgraph.graph import StateGraph, END
from orchestration.state import AgenticRAGState

from agents.planner.agent import PlannerAgent
from agents.retriever.agent import EvidenceRetrievalAgent
from agents.reasoner.agent import ReasonerAgent
from agents.verifier.agent import VerifierAgent

class AgenticRAGGraph:
    def __init__(self, verifier_threshold: float = 0.50):
        self.planner = PlannerAgent()
        self.retriever = EvidenceRetrievalAgent()
        self.reasoner = ReasonerAgent()
        self.verifier = VerifierAgent(threshold=verifier_threshold)
        
        # Build graph
        workflow = StateGraph(AgenticRAGState)
        
        workflow.add_node("planner", self._node_planner)
        workflow.add_node("retriever", self._node_retriever)
        workflow.add_node("reasoner", self._node_reasoner)
        workflow.add_node("verifier", self._node_verifier)
        
        workflow.set_entry_point("planner")
        workflow.add_edge("planner", "retriever")
        workflow.add_edge("retriever", "reasoner")
        workflow.add_edge("reasoner", "verifier")
        workflow.add_edge("verifier", END)
        
        self.app = workflow.compile()
        
    def _node_planner(self, state: AgenticRAGState):
        start = time.time()
        plan = self.planner.plan(state["question"])
        latency = (time.time() - start) * 1000
        
        return {
            "intent": plan.get("intent"),
            "complexity": plan.get("complexity"),
            "sub_queries": plan.get("sub_queries", []),
            "required_information": plan.get("required_information", []),
            "planner_metrics": {"latency_ms": latency}
        }
        
    def _node_retriever(self, state: AgenticRAGState):
        evidence_pkg = self.retriever.retrieve(
            request_id=state["request_id"],
            sub_queries=state["sub_queries"]
        )
        return {"evidence_package": evidence_pkg}
        
    def _node_reasoner(self, state: AgenticRAGState):
        reasoning_out = self.reasoner.reason(
            question=state["question"], 
            evidence_package=state["evidence_package"]
        )
        return {"reasoning_output": reasoning_out}
        
    def _node_verifier(self, state: AgenticRAGState):
        pkg = state["evidence_package"]
        reasoning = state["reasoning_output"]
        
        used_ids = set(reasoning.analysis.used_chunks)
        used_chunks = [c for c in pkg.chunks if c.chunk_id in used_ids]
        
        verifier_resp = self.verifier.verify(
            draft_answer=reasoning.answer,
            used_chunks=used_chunks,
            required_information=state["required_information"]
        )
        
        return {
            "verifier_response": verifier_resp,
            "final_answer": reasoning.answer
        }

    def invoke(self, question: str, request_id: str = "req_1") -> AgenticRAGState:
        initial_state = {
            "request_id": request_id,
            "question": question,
            "intent": None,
            "complexity": None,
            "sub_queries": [],
            "required_information": [],
            "planner_metrics": {},
            "evidence_package": None,
            "reasoning_output": None,
            "verifier_response": None,
            "final_answer": ""
        }
        
        return self.app.invoke(initial_state)
