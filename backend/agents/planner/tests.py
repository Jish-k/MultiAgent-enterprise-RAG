import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.planner.agent import PlannerAgent

def test_planner():
    print("Initializing Planner Agent...")
    planner = PlannerAgent()
    
    # Test a simple query
    print("\n--- Test 1: Simple Query ---")
    q1 = "How many casual leaves are allowed?"
    print(f"Question: {q1}")
    res1 = planner.plan(q1)
    print(f"Intent: {res1.get('intent')}")
    print(f"Sub-queries:")
    for sq in res1.get('sub_queries', []):
        print(f"  - {sq}")
    
    # Test a complex query
    print("\n--- Test 2: Complex Query ---")
    q2 = "How do I apply for maternity leave and who approves it?"
    print(f"Question: {q2}")
    res2 = planner.plan(q2)
    print(f"Intent: {res2.get('intent')}")
    print(f"Sub-queries:")
    for sq in res2.get('sub_queries', []):
        print(f"  - {sq}")
    
    # Test another complex query
    print("\n--- Test 3: IT Cross-Domain Query ---")
    q3 = "What happens if I violate the company's IT security policy?"
    print(f"Question: {q3}")
    res3 = planner.plan(q3)
    print(f"Intent: {res3.get('intent')}")
    print(f"Sub-queries:")
    for sq in res3.get('sub_queries', []):
        print(f"  - {sq}")

if __name__ == "__main__":
    test_planner()
