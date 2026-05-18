# Newcomer Task Lanes

## Docs-Only Lane

- Required reading: `docs/onboarding/source-of-truth-map.md`, `docs/architecture/project-document-freshness-policy.md`.
- Safe files: docs, tutorials, wiki source.
- Unsafe files: raw data, generated outputs.
- Validation: wiki validation, state-drift.
- Acceptance: no stale current-state claims and no raw/generated content.

## Test-Only Lane

- Required reading: `TESTING.md`.
- Safe files: `tests/python/`, small synthetic fixtures.
- Unsafe files: real raw corpora and generated outputs.
- Validation: focused pytest, full pytest when practical.
- Acceptance: tests fail for the intended regression and pass after the fix.

## Source-Lock Lane

- Required reading: `DATASET.md`, `docs/onboarding/private-generated-data-map.md`.
- Safe files: lock metadata, source records, schemas.
- Unsafe files: raw downloaded artefacts.
- Validation: lock-hash and source-record checks.
- Acceptance: hashes, URLs, acquisition notes, and trust flags are explicit.

## Observation Records Lane

- Required reading: `docs/onboarding/source-of-truth-map.md`, `RESULTS_SCHEMA.md`.
- Safe files: curated observation YAML/JSONL records.
- Unsafe files: raw images, raw Discord logs.
- Validation: observation validators and consistency checks.
- Acceptance: records are reviewable, source-backed, and not canonical unless explicitly scoped.

## Negative Controls Lane

- Required reading: `docs/experiments/method-retirement-ledger.md`.
- Safe files: negative-control records and tests.
- Unsafe files: broad experiment outputs.
- Validation: schema and method-retirement checks.
- Acceptance: false-positive class is preserved without creating a solve claim.

## CLI/Docs Lane

- Required reading: `docs/reference/cli-command-surface.md`, `docs/onboarding/codex-navigation-map.md`.
- Safe files: CLI docs and small command registration changes.
- Unsafe files: behavior-changing refactors without tests.
- Validation: CLI help tests and command-surface tests.
- Acceptance: command names/options stay stable unless explicitly scoped.

## Experiment Manifest Lane

- Required reading: `EXPERIMENTS.md`, `docs/roadmap/staged-plan.md`.
- Safe files: disabled manifests and schema tests.
- Unsafe files: generated results and raw data.
- Validation: manifest validation and operator policy checks.
- Acceptance: candidate bounds, output policy, no-solve flags, and stop conditions are explicit.

## Infrastructure Lane

- Required reading: `ARCHITECTURE.md`, `TESTING.md`, `docs/ci/anti-drift-checks.md`.
- Safe files: focused helpers, CI scripts, tests.
- Unsafe files: broad refactors and CUDA.
- Validation: full local validation stack.
- Acceptance: behavior stays compatible and raw-data-free CI remains intact.
