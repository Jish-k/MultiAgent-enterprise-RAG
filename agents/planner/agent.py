import json
import re
import sys
import os

# Add project root to path so we can import from llm
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from llm.provider import get_llm
from agents.planner.prompt import get_planner_prompt

class PlannerAgent:
    """
    Agent 1: The Query Planning Agent.
    Responsible for Intent Classification, Query Rewriting, and Query Decomposition.
    """
    def __init__(self):
        self.llm = get_llm()
        self.prompt = get_planner_prompt()
        self.chain = self.prompt | self.llm
        
    def plan(self, question: str) -> dict:
        """
        Takes a user question and returns a plan dictionary.
        Returns:
            {
                "intent": str,
                "sub_queries": list[str]
            }
        """
        response = self.chain.invoke({"question": question})
        content = response.content.strip()
        
        # Robust JSON extraction using regex in case the LLM adds conversational filler
        # Find the first { and the last }
        match = re.search(r'\{.*\}', content, re.DOTALL)
        
        if match:
            json_str = match.group(0)
            try:
                plan_dict = json.loads(json_str)
                # Ensure structure
                if "sub_queries" not in plan_dict or not isinstance(plan_dict["sub_queries"], list):
                    plan_dict["sub_queries"] = [question]
                if "intent" not in plan_dict:
                    plan_dict["intent"] = "Unknown"
                return plan_dict
            except json.JSONDecodeError:
                print(f"[PlannerAgent Warning] JSONDecodeError. Raw output: {content}")
        else:
            print(f"[PlannerAgent Warning] No JSON found in output. Raw output: {content}")
            
        # Fallback if parsing completely fails
        return {
            "intent": "Unknown",
            "sub_queries": [question]
        }
