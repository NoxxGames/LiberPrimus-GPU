# Project State And Source Of Truth

## Current Reviewed State

Stage 3V is complete, Stage 3W and Stage 3X are complete, Stage 3Y is complete, Stage 3Z is complete, Stage 4A is complete, and Stage 4B is complete. Stage 4C is the next planned cuneiform and dot annotation pack.

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
- `docs/roadmap/staged-plan.md`
- `docs/onboarding/start-here.md`
- `docs/onboarding/source-of-truth-map.md`

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
- `docs/onboarding/**`

Stage details:

- `docs/development-logs/**`
- `research-log/**`

Development logs and research logs are historical records. Do not rewrite old logs merely because they mention an old stage.

## Anti-Drift Policy

When stage status changes, update `STATUS.md`, `ROADMAP.md`, `AGENTS.md`, `README.md`, and `docs/roadmap/staged-plan.md` together.

When direction, experiment priority, method-family status, data policy, CLI behavior, or schema/result-family behavior changes, update the relevant `.md` and `.txt` files in the same stage. If no documentation needs updates, say why in the final report.

Long-lived operational docs must not describe obsolete stages as the current state. Stage-specific or historical docs may preserve old wording when it is clearly archival, such as "implemented since Stage 0A" or a dated development log.

The consistency suite includes a state-drift check for the operational docs and staged plan. It fails on stale current-state claims such as "current stage is Stage 0A", obsolete "no result schema" wording, missing staged-plan policy, or claims that CUDA/search/page-boundary policy has advanced beyond the documented safeguards.

## Onboarding Maps

Use these Stage 3Z maps for orientation:

- `docs/onboarding/start-here.md`: first read for humans.
- `docs/onboarding/source-of-truth-map.md`: authoritative files and historical/current distinction.
- `docs/onboarding/codex-navigation-map.md`: Codex read-order and update rules.
- `docs/onboarding/deep-research-handoff-map.md`: Deep Research handoff inputs and privacy boundaries.
- `docs/onboarding/contributor-module-map.md`: repo area to module map.
- `docs/onboarding/newcomer-task-lanes.md`: safe task lanes and validation commands.
- `docs/onboarding/private-generated-data-map.md`: private, raw, and generated data boundaries.

## Deferred Work

Deferred work after Stage 3Y:

- Stage 4A: full Discord research-bundle extraction for Deep Research.
- Stage 4B: website-derived source-lock triage and visual observation intake.
- Stage 4C: cuneiform and dot annotation pack.
- Stage 4D: OutGuess/audio historical fixture source-locking.
- Stage 4E: CPU batch transform API extraction.
- Stage 4F: scorer consolidation and calibration report.
- OutGuess historical fixture acquisition and source-locking.
- CUDA parity planning after CPU batch APIs and stable scoring contracts exist.
