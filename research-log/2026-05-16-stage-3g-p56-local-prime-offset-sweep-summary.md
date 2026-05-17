# Stage 3G p56-local prime offset sweep summary

Run ID: `stage3g-stage3e_prime_minus_one_offsets_v1-20260517T150902Z`

Stage 3G executed the bounded p56-local `prime_minus_one` offset sweep for `stage3e_prime_minus_one_offsets_v1`.

## Run Summary

- Input slice: `stage3a-page-candidate-018-reviewable-slice`
- Input length: `87`
- Offsets tested: `0..63`
- Directions tested: `forward`, `reverse`
- Reset modes tested: `none`, `line`
- Expected candidates: `256`
- Executed candidates: `256`
- Deferred candidates: `0`
- Top offset: `29`
- Top direction: `reverse`
- Top reset mode: `line`
- Top score: `1.36709`
- Top length-normalized score: `0.994247`
- Top calibrated confidence label: `inconclusive`
- Confidence distribution: `garbage=250`, `inconclusive=6`

The top lead is inconclusive and is not a solve claim. The score profile remains weak enough that follow-up should focus on controls, reset/advance ablation, or careful inspection rather than broadening into larger searches.

## Generated Outputs

Ignored local outputs are under:

- `experiments/results/bounded-auto-runs/stage3g/candidate_records.jsonl`
- `experiments/results/bounded-auto-runs/stage3g/top_candidates.jsonl`
- `experiments/results/bounded-auto-runs/stage3g/summary.json`
- `experiments/results/bounded-auto-runs/stage3g/calibrated_scores.jsonl`

Full candidate dumps are not committed.

## Mersenne Probe

Stage 3G also added `stage3i_mersenne_prime_stream_tiny_v1` to the method backlog and bounded queue as a future low-cost Mersenne/perfect-number stream probe. Candidate count is `192`. It remains `needs_executor` and was not executed in Stage 3G.

No CUDA was used. The canonical corpus remains inactive. Page boundaries remain reviewable. No solve claim is made.
