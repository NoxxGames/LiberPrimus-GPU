> This Wiki page mirrors $sourceRel. The repository tutorial file is the source of truth.

# Repository Tour

## Top-Level Docs

Start with `README.md`, `AGENTS.md`, `DATASET.md`, `RESEARCH.md`, `TESTING.md`, `RESULTS_SCHEMA.md`, `STATUS.md`, and `ROADMAP.md`.

## Data Folders

`data/raw/` contains ignored immutable local sources.

`data/locks/` contains committed SHA-256 and metadata locks.

`data/normalized/` contains ignored generated outputs.

## Python Modules

`python/libreprimus/legacy_workbook/` parses the non-canonical workbook.

`python/libreprimus/legacy_pastebin/` parses the non-canonical Pastebin TXT.

`python/libreprimus/transcript_sources/` parses transcript candidates.

`python/libreprimus/alignment/` emits Stage 0D alignment hints.

`python/libreprimus/profiles/` validates frozen Stage 0E profiles.

`python/libreprimus/corpus_candidate/` generates inactive corpus candidate records.

## Tests

Python tests live under `tests/python/`. They use synthetic fixtures and conditional real-source checks.

## Logs

`docs/development-logs/` records implementation work. `research-log/` records research-stage summaries.

## Public Docs

`tutorials/` is the user-facing learning path. `docs/github/` contains issue and wiki bootstrap support. `scripts/github/` contains GitHub helper scripts.

## Profiles And Schemas

`data/profiles/` contains committed tooling profiles. `schemas/corpus/` contains committed JSON schemas for Stage 0E generated records.
