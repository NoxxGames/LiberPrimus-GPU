# Bounded CPU Experiment Execution

## Purpose

Stage 2F adds the first execution harness for experiment manifests, but it is intentionally limited to synthetic inputs and solved-fixture replay.

## Why Stage 2F Permits Limited Execution

The project already has CPU reference transforms, solved baselines, result-store schemas, CI, consistency checks, and dry-run planning. Stage 2F uses that foundation to verify the mechanics of safe execution without touching unsolved pages.

## Allowed Scopes

- `synthetic_only`
- `solved_fixture_only`
- `synthetic_and_solved_fixture_only`

## Forbidden Scopes

Future unsolved page candidates, reviewable page spans, unresolved page boundaries, raw corpus slices, scoring campaigns, CUDA work, and search campaigns remain blocked.

## Safety Gates

Execution manifests must keep `unsolved_execution_allowed=false`, `search_execution_enabled=false`, `candidate_generation_enabled=false`, `scoring_enabled=false`, `cuda_enabled=false`, `canonical_corpus_active=false`, `page_boundaries_final=false`, and `trusted_as_canonical=false`.

## Registry Dispatch

Synthetic execution uses the Stage 2A CPU reference transform registry. A transform must be registered, CPU-reference supported, search disabled, and GPU disabled.

## Result Records

Generated `cpu_execution_plan`, `cpu_execution_result`, and summary records are written to ignored experiment result directories.

## Result-Store Integration

Stage 2F records result-store compatibility as preview metadata. JSONL and SQLite imports remain generated outputs and must not be committed.

## Non-Goals

Stage 2F does not run unsolved-page experiments, generate unsolved-page candidate plaintexts, score candidates, use CUDA, activate a canonical corpus, or finalize page boundaries.

## Future Transition

A later Stage 2G proposal must define the review and approval workflow before any bounded real exploratory run is allowed.
