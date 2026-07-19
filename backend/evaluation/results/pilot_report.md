# Milestone 2.5: Pilot Benchmark Analysis

## 1. Configuration Comparison

| Metric | Config A (Baseline) | Config B (Planner) | Config C (Agentic) | Config D (Plan+Gen) |
|---|---|---|---|---|
| Final Accuracy | 0.46 | 0.36 | 0.35 | 0.41 |
| Exact Match | 0.05 | 0.00 | 0.00 | 0.05 |
| Semantic Similarity | 0.28 | 0.24 | 0.24 | 0.29 |
| Citation Accuracy | 0.00 | 0.61 | 0.55 | 0.00 |
| ESS | 0.00 | 0.00 | 0.21 | 0.00 |
| Claim Support Rate | 0.00 | 0.00 | 0.46 | 0.00 |
| Hallucination Resistance | 0.00 | 0.00 | 0.36 | 0.00 |
| Avg Latency (ms) | 31783.27 | 76073.91 | 139558.09 | 35200.59 |
| Avg Tokens (Gen) | 327.15 | 397.98 | 359.82 | 449.95 |

## 2. Per-Category Performance (Final Accuracy)

| Category | Config A | Config B | Config C | Config D |
|---|---|---|---|---|
| Employee Handbook | 0.59 | 0.59 | 0.57 | 0.55 |
| Leave Policy | 0.49 | 0.50 | 0.46 | 0.46 |
| HR Policy | 0.30 | 0.34 | 0.31 | 0.30 |
| IT Security | 0.52 | 0.33 | 0.35 | 0.46 |
| Travel Policy | 0.41 | 0.15 | 0.15 | 0.21 |
| Expense Policy | 0.40 | 0.39 | 0.38 | 0.40 |
| Cross Document | 0.44 | 0.23 | 0.23 | 0.33 |
| Adversarial | 0.49 | 0.23 | 0.25 | 0.49 |

## 3. Error Analysis (Top 5 Worst-Performing Queries)

### Question ID: Q133 (Config B)
- **Final Score**: 0.01 (Exact: 0.00, Semantic: 0.04)
- **Question**: What is the annual salary of the CEO?
- **Expected Answer**: No expected documents specified. Out of domain.
- **Confidence**: 0.00
- **ESS**: 0.00

### Question ID: Q133 (Config B)
- **Final Score**: 0.01 (Exact: 0.00, Semantic: 0.04)
- **Question**: What is the annual salary of the CEO?
- **Expected Answer**: No expected documents specified. Out of domain.
- **Confidence**: 0.00
- **ESS**: 0.00

### Question ID: Q133 (Config C)
- **Final Score**: 0.01 (Exact: 0.00, Semantic: 0.04)
- **Question**: What is the annual salary of the CEO?
- **Expected Answer**: No expected documents specified. Out of domain.
- **Confidence**: 0.39
- **ESS**: 0.00

### Question ID: Q133 (Config C)
- **Final Score**: 0.01 (Exact: 0.00, Semantic: 0.04)
- **Question**: What is the annual salary of the CEO?
- **Expected Answer**: No expected documents specified. Out of domain.
- **Confidence**: 0.39
- **ESS**: 0.00

### Question ID: Q133 (Config B)
- **Final Score**: 0.01 (Exact: 0.00, Semantic: 0.04)
- **Question**: What is the annual salary of the CEO?
- **Expected Answer**: No expected documents specified. Out of domain.
- **Confidence**: 0.00
- **ESS**: 0.00

## 4. Confidence Calibration Table (Config C)

| Confidence Range | Average Accuracy | Count |
|---|---|---|
| <0.70 | 0.31 | 26 |
| 0.70-0.79 | 0.42 | 25 |
| 0.80-0.89 | 0.32 | 9 |
| 0.90-1.00 | nan | 0 |

## 5. Latency Distribution (End-to-End ms)

| Config | Mean | Median | Std Dev | Max |
|---|---|---|---|---|
| A | 31783 | 491 | 167854 | 949083 |
| B | 76074 | 1650 | 196362 | 914070 |
| C | 139558 | 2986 | 376086 | 1842521 |
| D | 35201 | 7359 | 157173 | 903753 |

## 6. Agent Contribution Matrix

| Metric | Baseline (A) | +Planner (B) | +Reasoner (D) | +Verifier (C) |
|---|---|---|---|---|
| Accuracy | 0.46 | 0.36 | 0.41 | 0.35 |
| Citation Accuracy | 0.00 | 0.61 | 0.00 | 0.55 |
| ESS | 0.00 | 0.00 | 0.00 | 0.21 |
| Context Tokens | 327.15 | 312.77 | 449.95 | 280.17 |
| Hallucination Rate | 0.00 | 0.00 | 0.00 | 0.36 |
| Avg Latency (ms) | 31783.27 | 76073.91 | 35200.59 | 139558.09 |