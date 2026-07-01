# Milestone 2.5: Pilot Benchmark Analysis

## 1. Configuration Comparison

| Metric | Config A (Baseline) | Config B (Planner) | Config C (Agentic) | Config D (Plan+Gen) |
|---|---|---|---|---|
| Final Accuracy | 0.48 | 0.34 | 0.35 | 0.42 |
| Exact Match | 0.05 | 0.00 | 0.00 | 0.05 |
| Semantic Similarity | 0.30 | 0.26 | 0.24 | 0.29 |
| Citation Accuracy | 0.00 | 0.57 | 0.59 | 0.00 |
| ESS | 0.00 | 0.00 | 0.00 | 0.00 |
| Claim Support Rate | 0.00 | 0.00 | 0.41 | 0.00 |
| Hallucination Resistance | 0.00 | 0.00 | 0.31 | 0.00 |
| Avg Latency (ms) | 2562.74 | 57487.80 | 316740.96 | 131458.69 |
| Avg Tokens (Gen) | 327.15 | 292.28 | 389.25 | 462.00 |

## 2. Per-Category Performance (Final Accuracy)

| Category | Config A | Config B | Config C | Config D |
|---|---|---|---|---|
| Employee Handbook | 0.60 | 0.40 | 0.58 | 0.55 |
| Leave Policy | 0.45 | 0.28 | 0.44 | 0.38 |
| HR Policy | 0.30 | 0.24 | 0.31 | 0.26 |
| IT Security | 0.55 | 0.35 | 0.38 | 0.45 |
| Travel Policy | 0.38 | 0.12 | 0.13 | 0.36 |
| Expense Policy | 0.44 | 0.26 | 0.37 | 0.43 |
| Cross Document | 0.56 | 0.21 | 0.31 | 0.47 |
| Adversarial | 0.49 | 0.10 | 0.10 | 0.49 |

## 3. Error Analysis (Top 5 Worst-Performing Queries)

### Question ID: Q137 (Config C)
- **Final Score**: 0.00 (Exact: 0.00, Semantic: 0.00)
- **Question**: Can employees carry firearms while travelling for business?
- **Expected Answer**: No expected documents specified. Out of domain.
- **Confidence**: 0.43
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
| <0.70 | 0.29 | 33 |
| 0.70-0.79 | 0.44 | 22 |
| 0.80-0.89 | 0.31 | 5 |
| 0.90-1.00 | nan | 0 |

## 5. Latency Distribution (End-to-End ms)

| Config | Mean | Median | Std Dev | Max |
|---|---|---|---|---|
| A | 2563 | 2491 | 2642 | 19010 |
| B | 57488 | 13503 | 189438 | 934862 |
| C | 316741 | 1797 | 947232 | 5514728 |
| D | 131459 | 801 | 315178 | 911363 |

## 6. Agent Contribution Matrix

| Metric | Baseline (A) | +Planner (B) | +Reasoner (D) | +Verifier (C) |
|---|---|---|---|---|
| Accuracy | 0.48 | 0.34 | 0.42 | 0.35 |
| Citation Accuracy | 0.00 | 0.57 | 0.00 | 0.59 |
| ESS | 0.00 | 0.00 | 0.00 | 0.00 |
| Context Tokens | 327.15 | 229.62 | 462.00 | 308.97 |
| Hallucination Rate | 0.00 | 0.00 | 0.00 | 0.31 |
| Avg Latency (ms) | 2562.74 | 57487.80 | 131458.69 | 316740.96 |