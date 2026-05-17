# Stage 3D Small Vigenere Key-List Summary

Date: 2026-05-16

## Run

- Run ID: `stage3d-stage3c-small-vigenere-known-motif-key-list-20260517T042442Z`
- Queue item: `stage3c-small-vigenere-known-motif-key-list`
- Input slice: `stage3a-page-candidate-018-reviewable-slice`
- Input length: `87`
- Candidate count: `4`
- Keys tested: `LIBER`, `PRIMUS`, `DIVINITY`, `CICADA`

## Top Lead

- Top key: `LIBER`
- Total score: `6.298395`
- Length-normalized score: `4.753506`
- Raw triage label: `garbage`
- Calibrated confidence label: `noisy`
- Crib hits: `0`

## Interpretation

The Stage 3D top candidate remains noisy under the Stage 3C calibrated scorer. The flat input stream warning is still present because separator context is unavailable for this selected slice. The result is not promising enough to treat as solve evidence.

## Generated Outputs

Full generated records remain ignored locally under:

- `experiments/results/bounded-auto-runs/stage3d/candidate_records.jsonl`
- `experiments/results/bounded-auto-runs/stage3d/top_candidates.jsonl`
- `experiments/results/bounded-auto-runs/stage3d/calibrated_scores.jsonl`
- `experiments/results/bounded-auto-runs/stage3d/summary.json`
- `experiments/results/bounded-auto-runs/stage3d/warnings.jsonl`

No full candidate dumps are committed. No solve claim is made.
