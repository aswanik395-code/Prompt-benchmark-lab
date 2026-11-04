# Scoring method (defined before running)

Each (prompt, test case) is run 3 times at temperature 0.7. Every run is scored on:

| Dimension | How it is scored |
|---|---|
| Correctness | Fraction of the 3 fields (category, urgency, reference_id) that exactly match `expected`. Averaged over runs. |
| Format compliance | 1 if the raw output parses as a bare JSON object (no prose, no code fences) with exactly the keys category/urgency/reference_id and valid enum values; else 0. |
| Hallucination | 1 if `reference_id` is non-null and does not appear in the complaint text (case-insensitive, leading # ignored). Reported as a count. |
| Consistency | Share of the 3 runs that produce the identical parsed JSON as the most common output. 1.0 = fully stable. |

Ground-truth rules: category = first issue mentioned; "high" urgency = safety risk, deadline < 24h, or total loss of access; tracking and phone numbers are not reference IDs.
