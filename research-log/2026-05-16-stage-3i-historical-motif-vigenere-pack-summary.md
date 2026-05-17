# Stage 3I Historical Motif Vigenere Pack Summary

Date: 2026-05-16

## Run

- Run ID: `stage3i-stage3e_vig_history_key_pack_v1-20260517T173351Z`
- Queue item: `stage3e_vig_history_key_pack_v1`
- Input slice: `stage3a-page-candidate-018-reviewable-slice`
- Input length: `87`
- Keys tested: `PATIENCEISAVIRTUE`, `THEINSTAREMERGENCE`, `SELFRELIANCE`, `BOOKOFTHELAW`, `MABINOGION`, `AGRIPPA`, `EMERSON`, `CROWLEY`, `BLAKE`, `PATIENCE`, `VIRTUE`, `SELF`, `RELIANCE`, `LAW`
- Reset modes tested: `none`, `line`
- Advance modes tested: `runes_only`, `token_break_preserving`
- Expected candidates: `56`
- Executed candidates: `56`
- Deferred candidates: `0`

## Top Lead

- Top key: `SELFRELIANCE`
- Top reset mode: `line`
- Top advance mode: `runes_only`
- Total score: `6.988031`
- Length-normalized score: `4.778141`
- Raw triage label: `garbage`
- Calibrated confidence label: `noisy`
- Crib hits: `0`

## Comparison To Stage 3F

Stage 3F LP evidence-key pack top lead was `EMERGE`, reset `none`, advance `runes_only`, score `6.800831`, calibrated label `noisy`.

Stage 3I historical motif key pack top lead has a slightly higher raw score, but the calibrated label remains `noisy` and the raw triage label is `garbage`. This does not materially improve on the Stage 3F result and is not solve evidence.

## Interpretation

The historical motif pack executed the full bounded manifest without deferred reset or advance modes. The result remains noisy under calibrated scoring. This supports moving to the next bounded method rather than expanding historical keys or starting a dictionary search.

## Generated Outputs

Full generated records remain ignored locally under:

- `experiments/results/bounded-auto-runs/stage3i/candidate_records.jsonl`
- `experiments/results/bounded-auto-runs/stage3i/top_candidates.jsonl`
- `experiments/results/bounded-auto-runs/stage3i/calibrated_scores.jsonl`
- `experiments/results/bounded-auto-runs/stage3i/summary.json`
- `experiments/results/bounded-auto-runs/stage3i/result_store_preview.json`

No full candidate dumps are committed. No solve claim is made.

