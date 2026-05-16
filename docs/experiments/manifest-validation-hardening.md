# Manifest Validation Hardening

## Purpose

Stage 2D hardens manifest validation before future CPU exploratory experiment
scaffolding. The checks confirm that current committed manifests are replayable
metadata, not search campaigns.

Stage 2E adds exploratory dry-run manifests to the same safety model.

## Solved-Baseline Manifests

Solved-baseline manifests under `experiments/manifests/solved-baselines/` must
validate against schema, point to existing fixture directories, and reference
registered CPU transform IDs.

## Result-Store Manifests

Result-store manifests under `experiments/manifests/result-store/` must validate
against schema and reference existing solved-baseline manifests by SHA-256.

## Registry Hash Validation

Solved-baseline manifests record the CPU transform registry SHA-256. Stage 2D
checks that the manifest value matches the committed registry bytes.

## Fixture Directory Validation

Each fixture group must point to an existing committed fixture directory and
declare the expected fixture count.

## Search/CUDA/Scoring False Flags

Manifests must keep `search_enabled=false`, `cuda_enabled=false`, and
`scoring_enabled=false`. Stage 2D does not introduce any campaign runner,
scorer, or GPU execution path.

Exploratory manifests additionally keep `execution_enabled=false`,
`search_execution_enabled=false`, `candidate_generation_enabled=false`, and
`dry_run_only=true`.

CPU execution manifests may set `execution_enabled=true` only for synthetic or
solved-fixture-only scopes. They still require
`unsolved_execution_allowed=false`, `search_execution_enabled=false`,
`candidate_generation_enabled=false`, `scoring_enabled=false`, and
`cuda_enabled=false`.

Stage 2G proposal files must keep execution, search, candidate generation,
scoring, CUDA, canonical corpus activation, and page-boundary finalization
disabled. Proposal review packets are generated outputs and must remain ignored.

## Generated Output Policy

Manifest-runner, result-store, and consistency outputs stay under ignored
`experiments/results/` locations. Generated summaries are useful for local
debugging but must not be staged.
