#!/bin/bash
source venv/bin/activate

echo "Running baseline..."
python backend/evaluation/scripts/run_hotpot_baseline.py

echo "Running stage 1..."
python backend/evaluation/scripts/run_agentic_stage1.py

echo "Running stage 2..."
python backend/evaluation/scripts/run_agentic_stage2.py

echo "Running stage 3..."
python backend/evaluation/scripts/run_agentic_stage3.py

echo "All evaluations finished!"
