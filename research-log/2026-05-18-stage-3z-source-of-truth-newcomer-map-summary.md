# Stage 3Z Source Of Truth And Newcomer Map Summary

Stage 3Z added durable onboarding maps for humans, Codex, Deep Research, contributors, and reviewers. No experiments were executed, no raw/generated outputs were committed, and no solve claim, CUDA change, canonical corpus activation, or page-boundary finalization was made.

## Onboarding Docs Created

- `docs/onboarding/README.md`
- `docs/onboarding/start-here.md`
- `docs/onboarding/source-of-truth-map.md`
- `docs/onboarding/codex-navigation-map.md`
- `docs/onboarding/deep-research-handoff-map.md`
- `docs/onboarding/contributor-module-map.md`
- `docs/onboarding/newcomer-task-lanes.md`
- `docs/onboarding/private-generated-data-map.md`

## Staged Plan And Direction Change

`docs/roadmap/staged-plan.md` now records Stage 3Y complete and Stage 3Z current/complete source-of-truth work. The planned Stage 4A direction is full Discord research-bundle extraction for Deep Research.

`data/research/project-direction-change-records-v0.yaml` now includes `stage3z-stage4-discord-bundle-priority`, documenting the shift from CPU batch API extraction as Stage 4A to Discord research-bundle extraction as Stage 4A. CPU batch API extraction remains planned later.

## Documentation Freshness

`AGENTS.md`, `docs/architecture/project-document-freshness-policy.md`, and `docs/architecture/project-state-and-source-of-truth.md` now point at the onboarding maps and require staged-plan/direction-change updates when project direction changes.

## Validation

- Focused Stage 3Z pytest: `19` passed.
- Focused ruff: passed.
- `libreprimus research-synthesis validate`: passed.
- `libreprimus consistency check-state-drift`: passed with `43` checks.
- Full pytest: `888` passed.
- Full ruff: passed.
- `libreprimus consistency check-all --allow-warnings`: passed with `481` checks.
- `libreprimus smoke`: passed.
- CI mirror scripts passed: run-consistency-checks, public docs status, lock hashes, workflow static validation, wiki validation, and wiki dry-run.

Generated output paths and raw third-party paths remained unstaged. Stage 3Z did not process Discord logs, page images, OutGuess artefacts, or experiment outputs.
