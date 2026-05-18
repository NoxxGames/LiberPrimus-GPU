# Stage 3S Onion 7 Seed Pack Development Log

## Purpose

Stage 3S executes only `EXP-3R-003`, the bounded Onion 7 explicit seed-pack manifest created in Stage 3R.

## Initial State

- Local HEAD matched `origin/main` at `5c2c81803a0aff037efa6911f9c932c9a3c39e1f`.
- Stage 3R manifests were present.
- Stage 3R promoted observation records were present.
- Raw Discord logs and raw page images were present locally but were not processed.
- Existing consistency, public-docs, lock-hash, workflow, and Wiki source checks passed before edits.

## Implementation

- Added `python/libreprimus/post_discord/` with manifest validation, Onion 7 value-space handling, route builders, stream application, export, summary, and validation helpers.
- Added `libreprimus post-discord validate-manifest`, `run-onion7-seed-pack`, and `summary`.
- Added Stage 3S consistency checks for the manifest and ignored post-Discord generated outputs.
- Kept raw Onion 7 values and derived values separated.
- Kept the run CPU-only, generated-output-ignored, and no-solve.

## Local Run

- Expected candidates: `72`
- Executed candidates: `72`
- Deferred candidates: `0`
- Top candidate: `raw_table`, `row_major`, `reverse`, reset `none`
- Top score: `1.460714`
- Calibrated confidence: `inconclusive`

Generated outputs remain ignored under `experiments/results/post-discord/stage3s/`.

## Tests And Validation

- Added Stage 3S tests for manifest validation, routes, executor behavior, CLI behavior, output fields, and ignore policy.
- Full validation was run before commit and push.

## Policy

Stage 3S does not execute `EXP-3R-001` or `EXP-3R-004`, process raw Discord logs, process raw page images, use OCR/AI/ML, use CUDA, activate canonical corpus, finalize page boundaries, or claim a solve.
