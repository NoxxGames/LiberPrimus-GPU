# Project State And Source Of Truth

## Current Reviewed State

Stage 3V is complete. Stage 3W consolidates repository state and adds anti-drift checks without adding experiment functionality.

The current safety posture is:

- No solve claim is made.
- The canonical corpus is inactive.
- Page boundaries are reviewable, not final.
- CUDA is deferred until CPU references, scorer definitions, batch APIs, parity tests, and benchmarks exist.
- Broad unsolved-page campaigns are not started.
- Raw data, generated outputs, SQLite databases, raw Discord logs, raw page images, raw historical stego artefacts, and extracted payloads are not committed.

## Authoritative File Hierarchy

Primary operational truth:

- `STATUS.md`
- `ROADMAP.md`
- `AGENTS.md`
- `README.md`

Research and workflow truth:

- `EXPERIMENTS.md`
- `RESULTS_SCHEMA.md`
- `TESTING.md`
- `DATASET.md`
- `RESEARCH.md`
- `CIPHER_CATALOG.md`

Architecture truth:

- `ARCHITECTURE.md`
- `CUDA_NOTES.md`
- `docs/architecture/**`
- `docs/ci/**`

User-facing guidance:

- `tutorials/**`
- `docs/wiki-source/**`
- `CONTRIBUTING.md`

Stage details:

- `docs/development-logs/**`
- `research-log/**`

Development logs and research logs are historical records. Do not rewrite old logs merely because they mention an old stage.

## Anti-Drift Policy

When stage status changes, update `STATUS.md`, `ROADMAP.md`, `AGENTS.md`, and `README.md` together.

Long-lived operational docs must not describe obsolete stages as the current state. Stage-specific or historical docs may preserve old wording when it is clearly archival, such as "implemented since Stage 0A" or a dated development log.

The consistency suite includes a state-drift check for the operational docs. It fails on stale current-state claims such as "current stage is Stage 0A", obsolete "no result schema" wording, or claims that CUDA/search/page-boundary policy has advanced beyond the documented safeguards.

## Deferred Work

Deferred work after Stage 3W:

- Stage 3X: CLI modularisation without behavior changes.
- Stage 3Y: result-synthesis and retirement ledger.
- Stage 3Z: source-of-truth and newcomer map expansion.
- Stage 4A: CPU batch transform API extraction.
- OutGuess historical fixture acquisition and source-locking.
- CUDA parity planning after CPU batch APIs and stable scoring contracts exist.
