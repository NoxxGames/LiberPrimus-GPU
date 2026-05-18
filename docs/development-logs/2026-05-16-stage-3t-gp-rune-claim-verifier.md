# Stage 3T GP/Rune Claim Verifier Development Log

## Purpose

Stage 3T executes only `EXP-3R-004`, the GP/rune claim verifier manifest created in Stage 3R.

## Initial State

- Local HEAD matched `origin/main` at `d2a5c668ea304954bb4fde9f7eac06f4f88fa007`.
- Stage 3S CI run `26047204489` passed.
- The Stage 3T manifest, Stage 3R promoted observation records, visual numeric observations, and Gematria profile were present.
- Raw Discord logs and raw page images were present locally but were not processed.
- Existing consistency, public-docs, lock-hash, workflow, and Wiki source checks passed before edits.

## Implementation

- Added `python/libreprimus/post_discord/gp_rune_claim_verifier.py`.
- Added CLI commands:
  - `post-discord validate-gp-rune-manifest`
  - `post-discord run-gp-rune-verifier`
  - `post-discord gp-rune-summary`
- Added Stage 3T consistency checks for manifest validation and ignored generated outputs.
- Added focused tests for manifest validation, claim loading/deduplication, computation, classification, CLI behavior, and ignore policy.

## Local Run

- Claims loaded: `25`
- Claims deduplicated: `25`
- Verified: `23`
- Unverified: `0`
- Boundary-sensitive: `0`
- Missing source span: `0`
- Unsupported: `2`
- Malformed: `0`
- Duplicate: `0`

Generated outputs remain ignored under `experiments/results/post-discord/stage3t/`.

## Policy

Stage 3T does not execute `EXP-3R-001`, rerun `EXP-3R-003`, search neighbouring spans, process raw Discord logs, process raw page images, use OCR/AI/ML, use CUDA, activate canonical corpus, finalize page boundaries, or claim a solve.

## Documentation And Validation

- Updated Stage 3T experiment, research, CLI, README/status/roadmap, tutorial, Wiki-source, testing, schema, and agent-policy documentation.
- Full Python tests passed: `789 passed`.
- Ruff passed for `python/libreprimus` and `tests/python`.
- CLI smoke, consistency checks, CI scripts, lock verification, workflow validation, Wiki source validation, and Wiki dry-run generation passed locally.
