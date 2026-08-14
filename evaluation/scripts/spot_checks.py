import csv
import json
from verifier.agent import VerifierAgent
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    with open('backend/evaluation/agentic_stage3_results.csv') as f:
        results = list(csv.DictReader(f))
        
    low_ess_rows = [r for r in results if float(r['ess']) < 1.0]
    
    print(f"Total Low ESS Rows (<1.0): {len(low_ess_rows)}\n")
    print("=== Entity-Confusion Spot Check (Low ESS) ===\n")
    
    for row in low_ess_rows[:3]:
        print(f"Q: {row['question']}")
        print(f"Expected: {row['expected_answer']}")
        print(f"Prediction: {row['prediction']}")
        print(f"ESS: {row['ess']}\n")
        
    print("=== Duplicate/Paraphrased Claim Check ===")
    print("Running ClaimExtractor on 2 samples...\n")
    
    agent = VerifierAgent()
    
    for row in low_ess_rows[:2]:
        claims = agent.extractor.extract(row['prediction'], row['question'])
        print(f"Q: {row['question']}")
        print(f"Prediction: {row['prediction']}")
        print("Extracted Claims:")
        for i, c in enumerate(claims):
            print(f"  {i+1}. {c}")
        print("\n")
        
if __name__ == "__main__":
    main()
