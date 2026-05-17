# Stage 3J Mersenne / Perfect-Number Probe Summary

Date: 2026-05-16

## Run

- Run ID: `stage3j-stage3j_mersenne_prime_stream_tiny_v1-20260517T181829Z`
- Queue item: `stage3j_mersenne_prime_stream_tiny_v1`
- Backlog item: `stage3i_mersenne_prime_stream_tiny_v1`
- Input slice: `stage3a-page-candidate-018-reviewable-slice`
- Input length: `87`
- Exponent sequence: `2`, `3`, `5`, `7`, `13`, `17`, `19`, `31`
- Stream variants: `mersenne_mod29`, `mersenne_minus_one_mod29`, `perfect_number_mod29`
- Offsets: `0..15`
- Directions: `forward`, `reverse`
- Reset modes: `none`, `line`
- Expected candidates: `192`
- Executed candidates: `192`
- Deferred candidates: `0`
- Unique stream signatures: `96`
- Duplicate stream signatures: `96`

## Top Lead

- Variant: `perfect_number_mod29`
- Offset: `3`
- Direction: `forward`
- Reset mode: `none`
- Total score: `1.515716`
- Length-normalized score: `1.122753`
- Raw triage label: `garbage`
- Calibrated confidence label: `inconclusive`

## Interpretation

The bounded Mersenne/perfect-number probe did not produce a strong lead. The top score is low, the raw triage label is `garbage`, and the calibrated label is only `inconclusive`.

Duplicate signatures were expected because the eight-exponent sequence is cyclic and offsets `0..15` include repeated phases. They were reported instead of being hidden or deduplicated.

This result does not justify broadening into arbitrary number-sequence search.

## Generated Outputs

Full generated records remain ignored locally under:

- `experiments/results/bounded-auto-runs/stage3j/candidate_records.jsonl`
- `experiments/results/bounded-auto-runs/stage3j/top_candidates.jsonl`
- `experiments/results/bounded-auto-runs/stage3j/calibrated_scores.jsonl`
- `experiments/results/bounded-auto-runs/stage3j/summary.json`
- `experiments/results/bounded-auto-runs/stage3j/result_store_preview.json`

No full candidate dumps are committed. No solve claim is made.

## Recommended Next Step

Stage 3K should create a visual numeric observation registry or archive-image source audit before turning page imagery, base-60 or cuneiform-like numbers, binary dot patterns, symmetry/asymmetry, or related observations into bounded experiment seeds.
