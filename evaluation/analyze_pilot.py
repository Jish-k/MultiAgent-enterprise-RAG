import os
import pandas as pd
import json

def generate_markdown_report():
    results_dir = "evaluation/results/pilot_v1.0"
    csv_path = os.path.join(results_dir, "pilot_benchmark_data.csv")
    breakdown_path = os.path.join(results_dir, "evaluation_breakdown.csv")
    out_path = "evaluation/results/pilot_report.md"
    
    if not os.path.exists(csv_path) or not os.path.exists(breakdown_path):
        print("Benchmark data not found. Ensure benchmark.py completed successfully.")
        return
        
    df = pd.read_csv(csv_path)
    b_df = pd.read_csv(breakdown_path)
    
    with open("evaluation/dataset/pilot_questions.json", "r") as f:
        pilot_questions = {q["id"]: q for q in json.load(f)}
    
    with open("evaluation/dataset/ground_truth.json", "r") as f:
        gt_data = {q["id"]: q for q in json.load(f)}
        
    # Add category to df
    df['category'] = df['id'].map(lambda x: pilot_questions.get(x, {}).get("category", "Unknown"))
    
    report = ["# Milestone 2.5: Pilot Benchmark Analysis\n"]
    
    # 1. Configuration Comparison Table
    report.append("## 1. Configuration Comparison\n")
    report.append("| Metric | Config A (Baseline) | Config B (Planner) | Config C (Agentic) | Config D (Plan+Gen) |")
    report.append("|---|---|---|---|---|")
    
    metrics = {
        'Final Accuracy': ('Final', b_df),
        'Exact Match': ('Exact', b_df),
        'Semantic Similarity': ('Semantic', b_df),
        'Citation Accuracy': ('Citation', b_df),
        'ESS': ('ESS', b_df),
        'Claim Support Rate': ('Claim Support Rate', b_df),
        'Hallucination Resistance': ('hallucination_resistance', df),
        'Avg Latency (ms)': ('e2e_latency_ms', df),
        'Avg Tokens (Gen)': ('generator_input_tokens', df)
    }
    
    for metric_name, (col, target_df) in metrics.items():
        row = [metric_name]
        for config in ['A', 'B', 'C', 'D']:
            if config in target_df['config'].values if 'config' in target_df else target_df['Config'].values:
                # Match config column name case
                c_col = 'config' if 'config' in target_df.columns else 'Config'
                val = target_df[target_df[c_col] == config][col].mean()
                row.append(f"{val:.2f}" if pd.notnull(val) else "0.00")
            else:
                row.append("-")
        report.append("| " + " | ".join(row) + " |")
        
    # 2. Per-Category Performance (Accuracy)
    report.append("\n## 2. Per-Category Performance (Final Accuracy)\n")
    report.append("| Category | Config A | Config B | Config C | Config D |")
    report.append("|---|---|---|---|---|")
    
    categories = df['category'].unique()
    for cat in categories:
        row = [cat]
        for config in ['A', 'B', 'C', 'D']:
            val = df[(df['category'] == cat) & (df['config'] == config)]['accuracy'].mean()
            row.append(f"{val:.2f}" if pd.notnull(val) else "-")
        report.append("| " + " | ".join(row) + " |")
        
    # 3. Error Analysis (Top 5 Worst)
    report.append("\n## 3. Error Analysis (Top 5 Worst-Performing Queries)\n")
    worst = b_df.sort_values(by='Final').head(5)
    for idx, row in worst.iterrows():
        qid = row['QID']
        config = row['Config']
        q_text = pilot_questions.get(qid, {}).get("question", "")
        expected = gt_data.get(qid, {}).get("expected_answer", "")
        
        report.append(f"### Question ID: {qid} (Config {config})")
        report.append(f"- **Final Score**: {row['Final']:.2f} (Exact: {row['Exact']:.2f}, Semantic: {row['Semantic']:.2f})")
        report.append(f"- **Question**: {q_text}")
        report.append(f"- **Expected Answer**: {expected}")
        report.append(f"- **Confidence**: {row.get('Confidence', df[(df['id']==qid) & (df['config']==config)]['confidence'].mean()):.2f}")
        report.append(f"- **ESS**: {row['ESS']:.2f}\n")
        
    # 4. Confidence Calibration (Config C only)
    report.append("## 4. Confidence Calibration Table (Config C)\n")
    report.append("| Confidence Range | Average Accuracy | Count |")
    report.append("|---|---|---|")
    
    conf_df = df[df['config'] == 'C'].copy()
    if not conf_df.empty and conf_df['confidence'].notnull().any():
        bins = [0.0, 0.7, 0.8, 0.9, 1.0]
        labels = ['<0.70', '0.70-0.79', '0.80-0.89', '0.90-1.00']
        conf_df['conf_bin'] = pd.cut(conf_df['confidence'], bins=bins, labels=labels, right=True)
        calibration = conf_df.groupby('conf_bin').agg(acc=('accuracy', 'mean'), count=('id', 'count')).reset_index()
        for idx, row in calibration.iterrows():
            report.append(f"| {row['conf_bin']} | {row['acc']:.2f} | {row['count']} |")
    else:
        report.append("| No confidence data generated | - | - |")
        
    # 5. Latency Distribution
    report.append("\n## 5. Latency Distribution (End-to-End ms)\n")
    report.append("| Config | Mean | Median | Std Dev | Max |")
    report.append("|---|---|---|---|---|")
    for config in ['A', 'B', 'C', 'D']:
        c_lat = df[df['config'] == config]['e2e_latency_ms']
        if not c_lat.empty:
            report.append(f"| {config} | {c_lat.mean():.0f} | {c_lat.median():.0f} | {c_lat.std():.0f} | {c_lat.max():.0f} |")
            
    # 6. Agent Contribution Matrix
    report.append("\n## 6. Agent Contribution Matrix\n")
    report.append("| Metric | Baseline (A) | +Planner (B) | +Reasoner (D) | +Verifier (C) |")
    report.append("|---|---|---|---|---|")
    
    metrics_acm = {
        'Accuracy': ('Final', b_df),
        'Citation Accuracy': ('Citation', b_df),
        'ESS': ('ESS', b_df),
        'Context Tokens': ('after_reasoner_tokens', df),
        'Hallucination Rate': ('hallucination_resistance', df),
        'Avg Latency (ms)': ('e2e_latency_ms', df)
    }
    
    for metric_name, (col, target_df) in metrics_acm.items():
        row = [metric_name]
        # Order: A, B, D, C
        for config in ['A', 'B', 'D', 'C']:
            if config in target_df['config'].values if 'config' in target_df else target_df['Config'].values:
                c_col = 'config' if 'config' in target_df.columns else 'Config'
                val = target_df[target_df[c_col] == config][col].mean()
                row.append(f"{val:.2f}" if pd.notnull(val) else "-")
            else:
                row.append("-")
        report.append("| " + " | ".join(row) + " |")
        
    with open(out_path, "w") as f:
        f.write("\n".join(report))
        
    print(f"Report generated at {out_path}")

if __name__ == "__main__":
    generate_markdown_report()
