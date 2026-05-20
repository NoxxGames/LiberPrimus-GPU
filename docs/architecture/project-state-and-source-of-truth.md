# Project State And Source Of Truth

## Current Reviewed State

Stage 3V is complete; Stage 3W through Stage 3Z are complete. Stage 4A through Stage 4Q are complete. Stage 5A through Stage 5E are complete. The next planned stage is Stage 5F first synthetic-only CUDA parity kernel implementation. Website expansion is deferred to Stage 6.

The current safety posture is:

- No solve claim is made.
- The canonical corpus is inactive.
- Page boundaries are reviewable, not final.
- CUDA is deferred until CPU references, scorer definitions, batch APIs, observation review workflow, promotion-ledger records, image-preflight controls, positive-control readiness, Stage 4O parity expectations, Stage 4P unified result surfaces, Stage 4Q benchmark planning, Stage 5A planning records, Stage 5B harness records, Stage 5C build/device records, Stage 5D native CPU parity records, Stage 5E first-kernel contract records, parity tests, and explicit Stage 5 implementation scope exist.
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

Current deferred work is tracked in `docs/roadmap/staged-plan.md` and the
research synthesis ledgers. The active near-term queue after Stage 4Q is:

- Stage 5A CUDA planning and parity scaffolding only.
- OutGuess/audio execution remains deferred until source-locked assets,
  expected outputs, and documented toolchains are available.
- CUDA implementation remains deferred until CPU batch APIs, stable scoring
  contracts, observation review gates, promotion-ledger records, image-preflight
  controls, positive-control readiness, Stage 4O parity expectations, Stage 4P
  unified result surfaces, Stage 4Q benchmark planning, parity tests, and explicit Stage 5 scope exist.
