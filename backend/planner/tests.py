import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from planner.agent import PlannerAgent

def test_planner():
    print("Initializing Planner Agent...")
    planner = PlannerAgent()
    
    # Test a simple query
    print("\n--- Test 1: Simple Query ---")
    q1 = "Who directed Big Stone Gap?"
    print(f"Question: {q1}")
    res1 = planner.plan(q1)
    print(f"Intent: {res1.get('intent')}")
    print(f"Sub-queries:")
    for sq in res1.get('sub_queries', []):
        print(f"  - {sq}")
    
    # Test a complex query
    print("\n--- Test 2: Complex Query ---")
    q2 = "The director of the romantic comedy 'Big Stone Gap' is based in what New York city?"
    print(f"Question: {q2}")
    res2 = planner.plan(q2)
    print(f"Intent: {res2.get('intent')}")
    print(f"Sub-queries:")
    for sq in res2.get('sub_queries', []):
        print(f"  - {sq}")
    
    # Test another complex query
    print("\n--- Test 3: Cross-Domain Query ---")
    q3 = "Which magazine was first started, Arthur's Magazine or First for Women?"
    print(f"Question: {q3}")
    res3 = planner.plan(q3)
    print(f"Intent: {res3.get('intent')}")
    print(f"Sub-queries:")
    for sq in res3.get('sub_queries', []):
        print(f"  - {sq}")

if __name__ == "__main__":
    test_planner()
