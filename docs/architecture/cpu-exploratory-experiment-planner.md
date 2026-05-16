# CPU Exploratory Experiment Planner

## Purpose

Stage 2E adds a dry-run-only planner for future bounded CPU exploratory experiments. It validates manifests, estimates candidate-count bounds, checks safety gates, and previews generated output paths without executing transforms.

## Dry-Run Only Design

Every Stage 2E exploratory manifest requires `dry_run_only=true` and keeps `execution_enabled`, `search_execution_enabled`, `candidate_generation_enabled`, `scoring_enabled`, and `cuda_enabled` set to `false`.

## Manifest Model

Exploratory manifests describe a corpus slice, transform-space preview, parameter bounds, result-store policy, output policy, provenance, and safety gates. They are committed YAML files under `experiments/manifests/exploratory/`.

## Candidate-Count Estimator

The estimator counts declared parameter spaces only. It supports singleton known transforms, Caesar previews, affine mod-29 previews, explicit Vigenere key lists, and explicit prime-stream parameter lists. It does not enumerate candidate plaintexts.

## Safety Gates

Safety gates reject enabled execution, search, candidate generation, scoring, CUDA, canonical corpus activation, page-boundary finalization, canonical trust, missing upper bounds, over-bound estimates, unreviewed future unsolved slices, and non-ignored repository output paths.

## Output Model

Generated dry-run plans are JSON and JSONL files under ignored result directories. They are planning records, not candidate results.

## Result-Store Preview

Stage 2E only previews result-store compatibility. It does not import exploratory records into SQLite or JSONL experiment stores.

## Non-Goals

Stage 2E does not run unsolved-page experiments, apply transforms, score candidates, use CUDA, activate a canonical corpus, or finalize page boundaries.

## Future Execution Stages

Future stages may design execution harnesses for synthetic or solved-fixture-only runs after dry-run manifests, result-store policy, and safety gates remain green in CI.
