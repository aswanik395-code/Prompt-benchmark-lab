## Which strategy won
Instruction-heavy won on every dimension: 0.96 correctness, 1.00 format, 1.00
consistency, 0 hallucinations. It was fully correct on 7 of 8 cases, including the
edge cases (multi-issue, tracking-number distractor, sarcasm) and it was not
fooled by the prompt injection in case 8.

## Patterns
- Basic (0.00 format): with no schema or allowed values, the model chose its own
  labels ("Billing", "Shipping Delay", "High") and sometimes added ```json fences.
  It still extracted reference IDs correctly, so most of its loss is format, not
  understanding.
- Few-shot (0.64 correctness): did well on cases like its examples (1, 3, 4) but
  invented labels where no example applied: "delivery" for shipping (case 2) and
  "customer_service" for sarcasm (case 7). My examples did not cover the
  shipping category, which is a flaw in my few-shot design, and shows few-shot
  teaches by example coverage, not by rules.
- Instruction-heavy: explicit enums, the "other" rule for sarcasm and the
  "tracking numbers are not IDs" rule fixed these failures. Its only miss was case 8:
  urgency "medium" vs my expected "low", a debatable call.
- No hallucinated reference IDs in any strategy (0 of 72 runs).
- Consistency rose with the amount of instruction: 0.67 -> 0.92 -> 1.00.

## Limitations
8 cases, 3 runs, one model, my own ground truth (case 8's urgency is debatable).
The scorer gives 0 correctness to unparseable output, so basic's correctness mixes
format and classification errors. The few-shot prompt lacked a shipping example,
which probably understated its performance.