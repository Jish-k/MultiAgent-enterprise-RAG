import matplotlib.pyplot as plt
import os

def generate_stage3_plots(recall_vals=[90.0, 100.0, 100.0], 
                          latencies=[282, 11, 2, 6, 3],
                          dedup_sizes=[33.3, 66.7]):
    """Generates the three specified plots for the paper."""
    
    out_dir = os.path.join(os.path.dirname(__file__), "results", "stage3")
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. Bar Chart: Recall@k
    k_labels = ['Recall@1', 'Recall@3', 'Recall@5']
    
    plt.figure(figsize=(6, 4))
    plt.bar(k_labels, recall_vals, color=['#4C72B0', '#55A868', '#C44E52'])
    plt.ylim(0, 110)
    plt.title('Retrieval Quality: Recall@k')
    plt.ylabel('Percentage (%)')
    for i, v in enumerate(recall_vals):
        plt.text(i, v + 2, f"{v}%", ha='center')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "recall_bar.png"))
    plt.close()
    
    # 2. Line Chart: Latency Breakdown
    components = ['Planner', 'Search', 'Merge', 'Dedup', 'Rank']
    
    plt.figure(figsize=(7, 4))
    plt.plot(components, latencies, marker='o', linestyle='-', color='#8C8C8C')
    plt.title('Agentic Pipeline Latency Breakdown')
    plt.ylabel('Time (ms)')
    plt.grid(True, linestyle='--', alpha=0.6)
    for i, txt in enumerate(latencies):
        plt.annotate(f"{txt}ms", (components[i], latencies[i] + max(latencies)*0.05))
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "latency_line.png"))
    plt.close()
    
    # 3. Pie Chart: Deduplication
    labels = ['Retained Evidence', 'Duplicates Removed']
    
    plt.figure(figsize=(5, 5))
    plt.pie(dedup_sizes, labels=labels, autopct='%1.1f%%', colors=['#4C72B0', '#DD8452'], startangle=140)
    plt.title('Evidence Quality: Deduplication')
    plt.savefig(os.path.join(out_dir, "dedup_pie.png"))
    plt.close()
    
    print(f"Plots saved successfully to: {out_dir}")

if __name__ == "__main__":
    generate_stage3_plots()
