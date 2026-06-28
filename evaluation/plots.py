import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def generate_plots():
    results_dir = "evaluation/results/pilot_v1.0"
    csv_path = os.path.join(results_dir, "pilot_benchmark_data.csv")
    
    if not os.path.exists(csv_path):
        print(f"Data not found at {csv_path}. Please run benchmark.py first.")
        return
        
    df = pd.DataFrame(pd.read_csv(csv_path))
    
    # IEEE Grayscale & Publication settings
    plt.rcParams.update({
        'font.size': 12, 
        'font.family': 'serif',
        'axes.prop_cycle': plt.cycler('color', ['#000000', '#555555', '#999999', '#CCCCCC']),
        'figure.autolayout': True
    })
    
    # 1. Ablation Bar Chart (Accuracy by Config with SD)
    ablation = df.groupby('config')['accuracy'].agg(['mean', 'std']).reset_index()
    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(ablation['config'], ablation['mean'], yerr=ablation['std'], capsize=5, color='gray', edgecolor='black', hatch='//')
    ax.set_ylabel('Mean Accuracy')
    ax.set_xlabel('Configuration')
    ax.set_title('Ablation Study: Accuracy by Configuration')
    ax.set_ylim(0, 1.1)
    
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f'{yval:.2f}', ha='center', va='bottom', fontsize=10)
    plt.savefig(os.path.join(results_dir, "ablation_accuracy.png"), dpi=300)
    plt.close()

    # 2. Confidence vs Correctness (Config C only)
    config_c = df[df['config'] == 'C'].copy()
    if not config_c.empty and config_c['confidence'].notnull().any():
        bins = [0, 0.7, 0.8, 0.9, 1.0]
        labels = ['<0.70', '0.70-0.80', '0.80-0.90', '0.90-1.00']
        config_c['conf_bin'] = pd.cut(config_c['confidence'], bins=bins, labels=labels, right=True)
        conf_acc = config_c.groupby('conf_bin')['accuracy'].mean().fillna(0)
        
        fig, ax = plt.subplots(figsize=(7, 5))
        bars = ax.bar(labels, conf_acc, color='darkgray', edgecolor='black')
        ax.set_ylabel('Accuracy')
        ax.set_xlabel('Confidence Range')
        ax.set_title('Accuracy by Verifier Confidence')
        ax.set_ylim(0, 1.1)
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f'{yval:.2f}', ha='center', va='bottom', fontsize=10)
        plt.savefig(os.path.join(results_dir, "confidence_vs_accuracy.png"), dpi=300)
        plt.close()

    # 3. Accuracy vs Retrieval Difficulty
    ret_diff = df.groupby('retrieval_difficulty')['accuracy'].mean().reindex(['Low', 'Medium', 'High']).fillna(0)
    fig, ax = plt.subplots(figsize=(6, 5))
    bars = ax.bar(ret_diff.index, ret_diff.values, color='lightgray', edgecolor='black', hatch='\\\\')
    ax.set_ylabel('Accuracy')
    ax.set_xlabel('Retrieval Difficulty')
    ax.set_title('Accuracy vs Retrieval Difficulty')
    ax.set_ylim(0, 1.1)
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f'{yval:.2f}', ha='center', va='bottom', fontsize=10)
    plt.savefig(os.path.join(results_dir, "accuracy_vs_retrieval_difficulty.png"), dpi=300)
    plt.close()

    # 4. Accuracy vs Reasoning Difficulty
    rea_diff = df.groupby('reasoning_difficulty')['accuracy'].mean().reindex(['Easy', 'Medium', 'Hard', 'Expert']).fillna(0)
    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(rea_diff.index, rea_diff.values, color='silver', edgecolor='black', hatch='xx')
    ax.set_ylabel('Accuracy')
    ax.set_xlabel('Reasoning Difficulty')
    ax.set_title('Accuracy vs Reasoning Difficulty')
    ax.set_ylim(0, 1.1)
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f'{yval:.2f}', ha='center', va='bottom', fontsize=10)
    plt.savefig(os.path.join(results_dir, "accuracy_vs_reasoning_difficulty.png"), dpi=300)
    plt.close()

    # 5. Context Size Compression (Config C)
    if not config_c.empty:
        ctx = config_c[['retriever_input_tokens', 'after_dedup_tokens', 'after_reasoner_tokens', 'generator_input_tokens']].mean()
        fig, ax = plt.subplots(figsize=(8, 5))
        labels = ['Retriever Input', 'After Dedup', 'After Reasoner', 'Generator Input']
        ax.plot(labels, ctx.values, marker='o', color='black', linestyle='-', linewidth=2, markersize=8)
        ax.set_ylabel('Average Tokens')
        ax.set_title('Context Size Compression Across Pipeline Stages')
        ax.grid(True, linestyle=':', alpha=0.6)
        plt.savefig(os.path.join(results_dir, "context_compression.png"), dpi=300)
        plt.close()

    # 6. Latency Splits Pie Chart (Config C)
    if not config_c.empty:
        lats = [
            config_c['retriever_latency_ms'].mean(),
            config_c['reasoner_latency_ms'].mean(),
            config_c['verifier_latency_ms'].mean(),
            config_c['generation_latency_ms'].mean() # Note: Reasoner config does not use generation_latency directly
        ]
        # Since reasoner wraps generation, generation_latency might be 0 for Config C.
        # Let's adjust to Planner, Retriever, Reasoner, Verifier
        lats = [
            config_c['planner_latency_ms'].mean(),
            config_c['retriever_latency_ms'].mean(),
            config_c['reasoner_latency_ms'].mean(),
            config_c['verifier_latency_ms'].mean()
        ]
        labels = ['Planner', 'Retriever', 'Reasoner', 'Verifier']
        
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(lats, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ffffff', '#cccccc', '#999999', '#666666'], wedgeprops={'edgecolor': 'black'})
        ax.axis('equal')
        ax.set_title('Percentage of Total Latency by Stage')
        plt.savefig(os.path.join(results_dir, "latency_splits.png"), dpi=300)
        plt.close()

    # 7. Spider/Radar Comparison
    try:
        breakdown_csv = os.path.join(results_dir, "evaluation_breakdown.csv")
        if os.path.exists(breakdown_csv):
            b_df = pd.DataFrame(pd.read_csv(breakdown_csv))
            # Aggregate metrics by config
            radar_data = b_df.groupby('Config')[['Final', 'Citation', 'ESS', 'Claim Support Rate']].mean().fillna(0)
            
            # For latency, we need the original df
            lat_data = df.groupby('config')['e2e_latency_ms'].mean()
            # Normalize latency so higher is better (e.g. 1 - (latency/max_latency))
            max_lat = lat_data.max()
            if max_lat > 0:
                radar_data['Efficiency'] = 1.0 - (lat_data / max_lat)
            else:
                radar_data['Efficiency'] = 0.0
                
            labels = ['Accuracy', 'Faithfulness (Citation)', 'ESS', 'Claim Support Rate', 'Efficiency']
            num_vars = len(labels)
            
            angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
            angles += angles[:1] # Close the loop
            
            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            
            colors = ['#cccccc', '#888888', '#444444', '#000000']
            linestyles = [':', '-.', '--', '-']
            
            for idx, config in enumerate(['A', 'B', 'C', 'D']):
                if config in radar_data.index:
                    values = radar_data.loc[config].tolist()
                    values += values[:1] # Close the loop
                    
                    name_map = {'A': 'Baseline', 'B': 'Planner', 'C': 'Full Agentic', 'D': 'Plan+Reasoner'}
                    ax.plot(angles, values, color=colors[idx], linewidth=2, linestyle=linestyles[idx], label=name_map.get(config, config))
                    ax.fill(angles, values, color=colors[idx], alpha=0.1)
                    
            ax.set_theta_offset(np.pi / 2)
            ax.set_theta_direction(-1)
            ax.set_thetagrids(np.degrees(angles[:-1]), labels)
            ax.set_ylim(0, 1.0)
            ax.set_title("Configuration Performance Analysis (Radar)", y=1.1)
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
            
            plt.savefig(os.path.join(results_dir, "radar_comparison.png"), dpi=300, bbox_inches='tight')
            plt.close()
    except Exception as e:
        print(f"Could not generate radar chart: {e}")

    print(f"IEEE Grayscale Plots successfully generated in {results_dir}")

if __name__ == "__main__":
    generate_plots()
