# Stage 3S Onion 7 Seed Pack

Stage 3S executes the Stage 3R manifest `EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml`.

This is a bounded CPU experiment over the reviewed Onion 7 4x4 number table and reviewed derived value spaces. It is not a broad number-theory search and does not use raw Discord logs, raw page images, OCR, AI/ML, CUDA, or cloud services.

## Scope

- Manifest: `experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml`
- Candidate cap: `144`
- Expected candidate count: `72`
- Value spaces: `raw_table`, `prime_delta_table`, `prime_order_table`
- Routes: `row_major`, `column_major`, `reverse_row_major`, `reverse_column_major`, `clockwise_spiral`, `counterclockwise_spiral`
- Directions: `forward`, `reverse`
- Reset modes: `none`, `line`

Raw table values and derived values stay separated. Derived tables are review inputs, not source truth.

## Command

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord run-onion7-seed-pack `
  --manifest experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml `
  --out-dir experiments/results/post-discord/stage3s `
  --top-k 25 `
  --allow-warnings
```

## Output Policy

Generated files are ignored:

- `experiments/results/post-discord/stage3s/candidate_records.jsonl`
- `experiments/results/post-discord/stage3s/top_candidates.jsonl`
- `experiments/results/post-discord/stage3s/summary.json`
- `experiments/results/post-discord/stage3s/warnings.jsonl`

Only summary documentation and tests are committed. Candidate plaintext and generated JSONL/JSON are not evidence of a solve.

## Stage 3S Result

The local Stage 3S run executed `72` candidates and deferred `0`. The top candidate used `raw_table`, `row_major`, `reverse`, and reset mode `none`, with score `1.460714` and calibrated confidence `inconclusive`.

No solve claim is made.
