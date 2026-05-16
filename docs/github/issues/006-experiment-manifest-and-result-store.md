# Implement experiment manifests and result storage

## Summary

Build manifest-driven experiment execution and result/provenance storage.

## Current Status

Experiment and result schema docs exist; no serious runner exists.

## Scope

YAML manifest validation, JSONL/SQLite result sinks, provenance fields, and dry-run behavior.

## Non-Goals

Do not run brute-force campaigns or treat candidates as solves.

## Deliverables

Manifest models, result writers, tests, and docs.

## Acceptance Criteria

Runs record source locks, transform chain, scores, controls, environment, and git commit.

## Safety/Provenance Rules

Generated results remain ignored unless explicitly promoted through review.

Suggested labels: stage-1, testing, data-provenance, safety

## Dependencies

Transform registry and corpus candidate records.

## Links

- `EXPERIMENTS.md`
- `RESULTS_SCHEMA.md`
