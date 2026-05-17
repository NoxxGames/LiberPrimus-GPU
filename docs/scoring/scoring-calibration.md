# Scoring Calibration

Stage 3C calibrates minimal triage scoring before any wider bounded method is run.

The calibration compares:

- Positive controls from known solved fixture plaintext and safe readable synthetic strings.
- Null controls from deterministic random and shuffled local strings.
- Negative controls from repeated, high-entropy, separatorless, and impossible-bigram-heavy strings.
- Stage 3A and Stage 3B candidate leads.

The result is a generated ignored `calibration_summary.json` with score ranges, thresholds, candidate classifications, and a recommended next bounded method.

Calibration is not solve evidence. It is only a guardrail for deciding whether current candidate leads are distinguishable from null or negative controls.

## Output Policy

Generated calibration JSON and JSONL files belong under `experiments/results/scoring-calibration/stage3c/` and must not be committed. Committed research logs may include score ranges, classifications, and next-step recommendations only.
