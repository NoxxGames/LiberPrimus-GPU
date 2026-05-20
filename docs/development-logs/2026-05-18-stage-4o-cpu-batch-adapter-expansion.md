# Stage 4O Development Log - CPU Batch Adapter Expansion

Date: 2026-05-18

## Scope

Stage 4O expands CPU batch adapter coverage and solved-fixture-safe parity records for future CUDA reference work. It is not a CUDA implementation, GPU benchmark, broad experiment, raw-data processing, canonical corpus activation, page-boundary finalisation, or solve-claim stage.

## Initial State

- Starting commit: `0188fc48416abb6d5bc196dbfd49a8b8b97c6219`.
- Branch: `main`.
- `origin/main` matched local `HEAD`.
- Latest visible CI before work: run `26132505543`, success.
- CPU batch package, Stage 4H manifests, solved fixtures, transform registry, and Stage 4I scoring records were present.
- Baseline validation passed for Stage 4N stego-positive-controls, Stage 4H CPU batch manifest validation, Stage 4I scoring records, path sanitisation, research synthesis, state drift, consistency, public docs, lock hashes, workflow static validation, and wiki-source validation.

## Output Policy

- Generated Stage 4O CPU batch records live under `experiments/results/cpu-batch/stage4o/` and remain ignored.
- The committed aggregate summary is `data/research/stage4o-cpu-batch-adapter-expansion-summary.yaml`.
- Raw data, generated outputs, CUDA/GPU code, review-only observations, Discord logs, page images, stego/audio artefacts, and solve claims are out of scope.

## Implementation

- Added Stage 4O schemas for adapter coverage, parity expectations, solved-fixture streams, score-summary compatibility, and aggregate summary.
- Added solved-fixture-safe stream helpers, adapter coverage builder, parity expectation writer, and parity-readiness summary generation under `python/libreprimus/cpu_batch/`.
- Extended `libreprimus cpu-batch` with `solved-fixture-parity`, `adapter-expansion`, `parity-readiness`, and `validate-stage4o`.
- Added three Stage 4O manifests under `experiments/manifests/cpu-batch/`.
- Kept Stage 4H commands and generated-output policy intact.

## Local Run

- Solved fixture streams discovered: `5`.
- Solved fixture streams executed: `5`.
- Skipped fixture streams: `0`.
- Transform adapters supported: `9`.
- Transform adapters missing/deferred: `2`.
- Candidates executed: `8`.
- Result records: `8`.
- Parity expectations written: `8`.
- Scoring compatible/unavailable: `8 / 0`.

## Tests And Docs

- Added Stage 4O tests for schemas, solved-fixture streams, adapter expansion, parity expectations, scoring compatibility, CLI behavior, and ignore policy.
- Updated staged plan, research synthesis records, CPU/CUDA parity docs, result schema policy, testing notes, cipher catalog, tutorials, wiki-source mirrors, and top-level status files.
- Added summary-only research logs for CPU batch adapter expansion and CPU/CUDA parity readiness.
