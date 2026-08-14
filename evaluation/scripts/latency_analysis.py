import csv
import statistics
import json

def analyze_latency():
    with open('backend/evaluation/agentic_stage3_results.csv', 'r') as f:
        results = list(csv.DictReader(f))
        
    latencies = [float(row['latency']) for row in results]
    
    mean_lat = statistics.mean(latencies)
    median_lat = statistics.median(latencies)
    max_lat = max(latencies)
    min_lat = min(latencies)
    
    print(f"Mean Latency: {mean_lat:.2f}s")
    print(f"Median Latency: {median_lat:.2f}s")
    print(f"Min Latency: {min_lat:.2f}s")
    print(f"Max Latency: {max_lat:.2f}s")
    print(f"\nRaw Latency List:\n{json.dumps([round(l, 2) for l in latencies])}")
    
    # Try to deduce retries: if latency > 100s, it's highly likely a rate limit or HTTP retry backoff occurred 
    # internally (e.g. within Langchain/Groq python SDK).
    # Since we can't definitively get the retry count from the CSV, we'll see the latency distribution.
    fast_questions = [l for l in latencies if l < 80]
    print(f"\nQuestions with latency < 80s (Likely 0 internal retries): {len(fast_questions)}")
    if fast_questions:
        print(f"Mean Latency of this subset: {statistics.mean(fast_questions):.2f}s")
        print(f"Median Latency of this subset: {statistics.median(fast_questions):.2f}s")

if __name__ == '__main__':
    analyze_latency()
