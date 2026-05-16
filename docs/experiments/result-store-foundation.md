# Result Store Foundation

## Purpose

Stage 2B adds durable result-store infrastructure before any unsolved-page experiment is allowed. The first importer handles the Stage 2A all-known solved-baseline manifest run.

## Result-Store Manifest

The committed manifest is `experiments/manifests/result-store/stage2b-solved-baseline-import.yaml`. It pins the Stage 2A solved-baseline manifest, expected run kind, output paths, and false search/scoring/CUDA flags.

## Stage 2B Solved-Baseline Import

The importer reads:

- `experiments/results/solved-baselines/stage2a/summary.json`
- `experiments/results/solved-baselines/stage2a/manifest_run_records.jsonl`
- `experiments/results/solved-baselines/stage2a/warnings.jsonl`

If Stage 2A results are missing, the Stage 2B smoke command can regenerate them through the solved-baseline runner.

## Generated Outputs

Stage 2B writes generated outputs under `experiments/results/result-store/stage2b/`:

- `run_records.jsonl`
- `event_records.jsonl`
- `artifact_records.jsonl`
- `summary.json`
- `results.sqlite3`

These outputs remain ignored and must not be committed.

## SQLite Schema

The SQLite store contains `schema_metadata`, `runs`, `events`, `artifacts`, and `summaries`. The detailed record remains JSON text, while key fields such as `run_id`, `manifest_id`, `registry_id`, `git_commit`, and false safety flags are indexed columns.

## JSONL Schema

JSONL records validate against schemas under `schemas/results/`. The schemas enforce non-canonical status and reject solved-baseline imports that claim search, scoring, CUDA, or canonical trust.

## Run Provenance

Run provenance includes manifest SHA-256, registry SHA-256, git commit, branch, platform, Python version, profile hashes, fixture counts, and generated artifact metadata.

## What This Enables

The project can now preserve solved-baseline regression runs in machine-readable result stores that future CI or review tools can validate.

## What It Does Not Enable

Stage 2B does not define search spaces, score candidates, run CUDA, activate a canonical corpus, finalize page boundaries, or provide solve evidence for unsolved pages.
