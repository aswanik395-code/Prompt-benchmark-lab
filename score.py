"""Scores results/raw_outputs.json per SCORING.md and writes results/results_table.md."""
import json
from collections import Counter, defaultdict

CATS = {"billing", "shipping", "product_defect", "account_access", "other"}
URG = {"low", "medium", "high"}
cases = {c["id"]: c for c in json.load(open("test_cases.json"))}
data = json.load(open("results/raw_outputs.json"))["runs"]

def parse(s):
    try:
        o = json.loads(s)
        return o if isinstance(o, dict) else None
    except Exception:
        return None

def score(run):
    c, o = cases[run["case_id"]], parse(run["output"])
    fmt = int(bool(o) and set(o) == {"category", "urgency", "reference_id"}
              and o["category"] in CATS and o["urgency"] in URG)
    if not o:
        return dict(correct=0.0, fmt=0, halluc=0, sig=None)
    exp = c["expected"]
    correct = sum(o.get(k) == exp[k] for k in exp) / 3
    ref = o.get("reference_id")
    halluc = int(ref is not None and str(ref).lstrip("#").lower() not in c["text"].lower())
    return dict(correct=correct, fmt=fmt, halluc=halluc, sig=json.dumps(o, sort_keys=True))

per = defaultdict(lambda: defaultdict(list))
for r in data:
    per[r["prompt"]][r["case_id"]].append(score(r))

lines = ["| Prompt | Case | Correctness | Format | Hallucinations | Consistency |", "|---|---|---|---|---|---|"]
summary = {}
for p, cs in per.items():
    agg = defaultdict(list)
    for cid, runs in sorted(cs.items()):
        corr = sum(x["correct"] for x in runs) / len(runs)
        fmt = sum(x["fmt"] for x in runs) / len(runs)
        hal = sum(x["halluc"] for x in runs)
        sigs = [x["sig"] for x in runs]
        cons = Counter(sigs).most_common(1)[0][1] / len(sigs)
        lines.append(f"| {p} | {cid} | {corr:.2f} | {fmt:.2f} | {hal} | {cons:.2f} |")
        for k, v in [("corr", corr), ("fmt", fmt), ("hal", hal), ("cons", cons)]:
            agg[k].append(v)
    summary[p] = {k: (sum(v) if k == "hal" else sum(v) / len(v)) for k, v in agg.items()}
lines += ["", "| Prompt | Mean correctness | Mean format | Total hallucinations | Mean consistency |", "|---|---|---|---|---|"]
for p, s in summary.items():
    lines.append(f"| {p} | {s['corr']:.2f} | {s['fmt']:.2f} | {s['hal']} | {s['cons']:.2f} |")
open("results/results_table.md", "w").write("\n".join(lines))
print("\n".join(lines))
