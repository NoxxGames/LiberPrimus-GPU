# Stage 3F Evidence-Key Vigenere Pack

## Goal

Stage 3F turns the highest-priority Stage 3E Vigenere queue item into a real bounded CPU execution without widening into key search.

## Inputs

- Queue: `experiments/queues/stage3e-bounded-cpu-queue.yaml`
- Item: `stage3e_vig_lp_evidence_pack_v1`
- Slice: `stage3a-page-candidate-018-reviewable-slice`
- Calibration: Stage 3C calibrated minimal triage scoring

## Execution Summary

- Expected candidates: `48`
- Executed candidates: `48`
- Deferred candidates: `0`
- Top key: `EMERGE`
- Top reset mode: `none`
- Top advance mode: `runes_only`
- Top calibrated confidence label: `noisy`

## Interpretation

The executor successfully records key, reset, and advance semantics for every candidate. The top candidate remains a lead only and does not justify a solve claim. Since the result is still noisy, the next bounded stage should prioritize the p56-local prime-minus-one offset sweep rather than broadening Vigenere search.

## Output Policy

Full candidate outputs stay ignored under `experiments/results/bounded-auto-runs/stage3f/`. Only summary-level research notes are committed.
