# Stage 4G Cookie Exact-Candidate Refresh Development Log

## Scope

Stage 4G implements and runs a bounded exact-hash candidate refresh for the historical Cicada cookie
artefacts using only Stage 4B source-backed candidate records and existing cookie target records.

Non-goals:

- broad hash cracking
- fuzzy or partial hash matching
- hashcat or GPU/CUDA
- dictionary expansion
- live Tor or live web scraping
- raw Discord or raw page-image processing
- solve claims

## Implementation

Added:

- `libreprimus.cookie_refresh`
- `libreprimus cookie-refresh run`
- `libreprimus cookie-refresh validate`
- `libreprimus cookie-refresh summary`
- Stage 4G cookie-refresh schemas
- committed aggregate summary
- focused tests and CI consistency integration

The real Stage 4G run used raw UTF-8 strings and SHA-256 only because the Stage 4B manifest does not
declare additional byte variants or algorithms.

## Local Run

- Target cookies: `2`
- Source-backed base strings: `4`
- Byte variants: `1`
- Algorithms: `sha256`
- Generated candidates before deduplication: `4`
- Candidates after deduplication: `4`
- Duplicate candidates: `0`
- Previous-pack duplicates: `2`
- Comparisons: `8`
- Exact matches: `0`

Generated outputs remain ignored under `experiments/results/cookie-refresh/stage4g/`.

## Follow-Up State

The cookie SHA-256 exact-pack family remains negative/deprioritised unless new exact source-backed
candidate strings appear. The next planned stage is Stage 4H CPU batch transform API extraction.

## Validation

Local validation run:

- `libreprimus cookie-refresh validate`: passed.
- `libreprimus research-synthesis validate`: passed.
- `libreprimus consistency check-state-drift`: passed.
- `libreprimus consistency check-all --allow-warnings`: passed.
- `libreprimus smoke`: passed.
- `ruff check python/libreprimus tests/python`: passed.
- `pytest -q tests/python`: passed, `981` tests.
- `scripts/ci/run-consistency-checks.ps1`: passed.
- public docs, lock hashes, workflow static validation, and Wiki dry-run validation passed.

Git safety checks confirm generated outputs and raw data remain unstaged.
