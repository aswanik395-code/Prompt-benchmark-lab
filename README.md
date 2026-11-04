# Prompt Benchmark Lab

Task: classify customer complaints into category, urgency and reference ID (JSON).
Compared: basic vs few-shot vs instruction-heavy prompts (`prompts.py`) on 8 cases (`test_cases.json`), including 5 edge cases: multi-issue, distractor numbers, sarcasm, prompt injection, safety.

## Run
    pip install groq
    export GROQ_API_KEY=your_key   # keep it out of the repo
    python run_benchmark.py   # saves results/raw_outputs.json
    python score.py           # saves results/results_table.md

Scoring method: `SCORING.md`. Final write-up: `ANALYSIS.md` (written after you have real results).
