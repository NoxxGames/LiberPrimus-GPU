# Stage 3T GP/Rune Claim Verifier Summary

Manifest: `experiments/manifests/post-discord/EXP-3R-004-gp-rune-claim-verifier-a.yaml`

Run ID: `stage3t-exp-3r-004-20260518T172432Z`

## Counts

- Claim cap: `64`
- Claims loaded: `25`
- Claims deduplicated: `25`
- Verified claims: `23`
- Unverified claims: `0`
- Boundary-sensitive claims: `0`
- Missing-source-span claims: `0`
- Unsupported claims: `2`
- Malformed claims: `0`
- Duplicate claims: `0`

## Representative Claim IDs

Verified examples:

- `stage3r-observation-cuneiform-pages-34-40-pairwise_17_13_base60`
- `stage3r-observation-cuneiform-pages-34-40-pairwise_55_1_base60`
- `stage3r-observation-cuneiform-pages-34-40-full_base60`
- `lp-cuneiform-sexagesimal-candidate-v0-full_base60_mod29`
- `historical-prime-dimensions-2016-v0-value-0-prime`

Unsupported examples:

- `stage3r-observation-dot-motifs-unsupported`
- `stage3r-observation-dead-oak-motif-unsupported`

## Interpretation

The verified records are exact arithmetic or prime-status recomputations over committed review records. They do not make Discord claims true as source evidence, do not activate a canonical corpus, and do not claim any solve. Unsupported visual motif records remain review material because they have no exact GP/rune claim to recompute.

## Generated Outputs

Ignored output paths:

- `experiments/results/post-discord/stage3t/gp_rune_claim_verification_records.jsonl`
- `experiments/results/post-discord/stage3t/verified_claims.jsonl`
- `experiments/results/post-discord/stage3t/unverified_claims.jsonl`
- `experiments/results/post-discord/stage3t/boundary_sensitive_claims.jsonl`
- `experiments/results/post-discord/stage3t/missing_source_span_claims.jsonl`
- `experiments/results/post-discord/stage3t/unsupported_claims.jsonl`
- `experiments/results/post-discord/stage3t/summary.json`

No full generated dumps are committed. No raw Discord logs or raw page images were processed. No solve claim is made.
