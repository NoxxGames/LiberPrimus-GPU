# Schema And Manifest Consistency

## Purpose

Stage 2D defines consistency checks that keep the CPU transform registry,
schemas, manifests, docs, ignored-output rules, and result-store metadata in
sync. Stage 2E extends those checks to exploratory dry-run schemas and
manifests before any execution harness is designed.

## Registry Consistency

The registry check validates transform IDs, alias targets, SHA locks,
fixture-set paths, and disabled search/CUDA/scoring flags. Registry transform
IDs must also appear in `CIPHER_CATALOG.md`.

## Manifest Consistency

Solved-baseline manifests must reference valid fixture directories and known
transform IDs. Result-store manifests must reference valid solved-baseline
manifests and preserve false search/CUDA/scoring flags. Exploratory manifests
must validate as dry-run-only, preserve disabled execution flags, and keep
candidate-count estimates within declared upper bounds.

CPU execution manifests must validate as synthetic-only or solved-fixture-only
execution, preserve disabled search/candidate-generation/scoring/CUDA flags, and
keep the blocked unsolved negative manifest as an expected validation failure.

## Schema Consistency

Schema files must parse as JSON, expected corpus/result/experiment schemas must
exist, and schema metadata must remain unique. Generated/non-canonical record
schemas keep `trusted_as_canonical=false`.

## Documentation Consistency

README, STATUS, and ROADMAP must agree on the current stage and next stage.
AGENTS.md must preserve raw-data, generated-output, CI, and push safety rules.
Cipher documentation must not claim search or CUDA support that the registry
does not provide.

## Ignored-Output Consistency

Raw corpus locations, generated normalized outputs, generated experiment
results, and SQLite databases must be ignored. Committed profiles, fixtures,
schemas, and manifests must remain trackable.

## Result-Store Consistency

The result-store check validates the Stage 2B manifest and result-store schemas.
If local generated result-store outputs exist, it validates JSONL and SQLite
counts. If they are absent, the check reports a warning instead of failing.

## Trust Boundaries

Stage 2G proposal consistency checks validate proposal and approval-record
schemas, require committed proposals to remain non-executable and unapproved,
and verify generated review packet paths are ignored.

The consistency suite is not source evidence and does not prove any page solve.
It is a CI gate that verifies committed metadata and documentation are internally
coherent.
