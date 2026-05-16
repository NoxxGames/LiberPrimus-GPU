# Experiment Result Store

## Status

Stage 2B implements the first result-store foundation for solved-baseline regression imports.

## Purpose

The result store records experiment-run provenance and generated artifacts in replayable JSONL and SQLite forms. It is infrastructure only: it does not run search, score candidates, claim solves, activate the corpus, or finalize page boundaries.

## JSONL Sink

The JSONL sink writes one UTF-8 JSON object per line with stable key ordering and schema validation before write. Stage 2B writes run, event, artifact, and summary records under `experiments/results/result-store/stage2b/`.

## SQLite Sink

The SQLite sink uses Python stdlib `sqlite3` and creates `schema_metadata`, `runs`, `events`, `artifacts`, and `summaries` tables. Detailed payloads are stored as JSON text, with key run fields indexed as ordinary columns for quick validation.

## Run Records

Run records capture run ID, manifest ID and SHA-256, registry ID and SHA-256, git commit, branch, host metadata, Python version, profile/source identifiers, fixture counts, transform counts, artifact references, warnings, and validation status.

## Event Records

Event records capture ordered warnings and informational events for the imported run. They are not source evidence and keep `trusted_as_canonical=false`.

## Artifact Records

Artifact records describe generated files imported into the result store. Stage 2B artifact records require `committed=false` and `ignored_by_git=true`.

## Provenance Model

The provenance collector records only bounded metadata: git commit, branch, platform, Python version, manifest hashes, registry hashes, and known profile hashes. It does not dump environment variables or secrets.

## Validation Rules

Solved-baseline imports require:

- `canonical_corpus_active=false`
- `page_boundaries_final=false`
- `search_performed=false`
- `scoring_used=false`
- `cuda_used=false`
- `trusted_as_canonical=false`

JSONL and SQLite counts must agree.

## Generated-Output Policy

All JSONL, JSON, and SQLite outputs under `experiments/results/result-store/` are generated and ignored. Schemas, manifests, code, tests, and docs are committed.

## Non-Canonical Status

The result store preserves solved-baseline regression evidence only. It does not make the rtkd candidate canonical and does not promote reviewable page boundaries.

## Future Extension Points

Future stages can add result importers for bounded CPU experiments, benchmark result stores, or review summaries after schemas and CI checks are stable.
