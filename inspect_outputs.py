import json
runs = json.load(open("results/raw_outputs.json"))["runs"]
want = [("basic",1),("basic",2),("few_shot",2),("few_shot",7),("instruction_heavy",8)]
for r in runs:
    if (r["prompt"], r["case_id"]) in want and r["run"] == 1:
        print(f"--- {r['prompt']} case {r['case_id']} ---")
        print(r["output"][:400], "\n")