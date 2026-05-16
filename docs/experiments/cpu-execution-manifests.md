# CPU Execution Manifests

## Manifest Fields

Stage 2F manifests use `record_type=cpu_execution_manifest`, `experiment_stage=stage2f`, `execution_enabled=true`, and a restricted `execution_scope`.

## Synthetic Manifests

Synthetic manifests carry small inline `synthetic_corpus_record` payloads. These records are safe for execution and must declare `contains_liber_primus_unsolved_text=false`.

## Solved Fixture Replay Manifest

The solved-fixture replay manifest references the Stage 2A all-known solved-baseline manifest and expects ten known solved fixture passes.

## Blocked Unsolved Manifest

`stage2f-blocked-unsolved-example.yaml` is a negative-control manifest. It is committed so tests can prove that future unsolved page candidate execution is rejected.

## Safety Flags

Search, candidate generation, scoring, CUDA, canonical corpus activation, page-boundary finalization, and canonical trust flags must remain false.

## Output Policy

Generated plans, result JSONL, summaries, SQLite files, and imports belong under ignored result directories and must not be committed.
