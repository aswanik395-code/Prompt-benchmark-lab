"""Runs every test case x prompt x N runs on Groq and saves raw outputs.
Setup: pip install groq ; export GROQ_API_KEY=your_key  (never commit the key)."""
import json, os, time
from groq import Groq
from prompts import PROMPTS

MODEL = "openai/gpt-oss-120b"
RUNS = 3
TEMPERATURE = 0.7
client = Groq(api_key=os.environ["GROQ_API_KEY"])
cases = json.load(open("test_cases.json"))
raw = []
for name, tmpl in PROMPTS.items():
    for c in cases:
        for r in range(RUNS):
            for attempt in range(3):
                try:
                    resp = client.chat.completions.create(
                        model=MODEL, max_tokens=300, temperature=TEMPERATURE,
                        messages=[{"role": "user", "content": tmpl.format(text=c["text"])}])
                    break
                except Exception as e:  # e.g. rate limit: wait and retry
                    print("retrying:", e); time.sleep(5 * (attempt + 1))
            else:
                raise SystemExit("failed after retries")
            raw.append({"prompt": name, "case_id": c["id"], "run": r + 1,
                        "output": resp.choices[0].message.content or ""})
            print(name, c["id"], r + 1)
json.dump({"model": MODEL, "temperature": TEMPERATURE, "runs": raw},
          open("results/raw_outputs.json", "w"), indent=2)
