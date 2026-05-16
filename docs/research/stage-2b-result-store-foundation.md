# Stage 2B Result Store Foundation

## Status

Complete. Stage 2B imports the Stage 2A solved-baseline regression output into generated JSONL and SQLite result stores.

## Stage Goal

Create a reusable result-store foundation with run records, events, artifacts, summaries, provenance capture, and validation before any unsolved-page experiment work begins.

## Inputs

- Stage 2A solved-baseline manifest: `experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml`
- Stage 2A generated solved-baseline outputs under `experiments/results/solved-baselines/stage2a/`
- CPU transform registry `cpu-reference-transforms-v0`
- Stage 0E profiles and inactive `rtkd-master-v0-candidate`

## Result-Store Design

The implementation provides two generated sinks:

- JSONL records for line-oriented review and deterministic diffs outside Git.
- SQLite records for structured local queries and future tooling.

Both sinks store the same Stage 2B run provenance and keep safety flags false.

## Generated Records

Stage 2B generates one `experiment_run_record`, warning/event records, artifact records for imported generated files, and one summary record.

## Stage 2A Import Result

The imported solved-baseline run records pass/fail/pending/skipped `10/0/0/0`. It preserves direct translation, Atbash-family, Vigenere, and prime-stream pass counts from the Stage 2A manifest runner.

## Validation Result

Validation checks JSONL schemas, SQLite table presence, JSONL/SQLite count agreement, generated-artifact flags, and false canonical/search/scoring/CUDA flags.

## What This Stage Proves

Stage 2B proves that a known solved-baseline regression run can be imported into durable generated result stores with provenance and schema validation.

## What This Stage Does Not Prove

It does not solve new pages, run unsolved-page experiments, implement scoring, implement search, use CUDA, activate a canonical corpus, or finalize page boundaries.

## Next Stage

Recommended next work: Stage 2C CI hardening for Python tests, ruff, schema validation, and CPU-only smoke commands, or bounded CPU experiment-manifest scaffolding after result-store validation.
