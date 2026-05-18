# Stage 3Z Source Of Truth And Newcomer Map

Date: 2026-05-19

## Initial State

- Branch: `main`
- Starting HEAD: `fbc2e9decd5b66a78237a6bb222f440e80f9f6d1`
- `origin/main`: `fbc2e9decd5b66a78237a6bb222f440e80f9f6d1`
- Local equals origin/main: true
- Latest known CI: GitHub Actions run `26064919234`, passed after Stage 3Y.
- Existing research-synthesis validation: passed.
- Existing state-drift check: passed with 27 checks.
- Raw/generated staged at start: 0.
- Onboarding docs directory present at start: false.

## Phase 1 - Onboarding Maps

- Created `docs/onboarding/README.md`.
- Created `start-here`, source-of-truth, Codex navigation, Deep Research handoff, contributor module, newcomer task-lane, and private/generated data maps.
- The maps preserve no-solve, canonical corpus inactive, page-boundary reviewable, CUDA deferred, and raw/generated non-commit policy.

## Phase 2 - Staged Plan And Direction Change

- Updated `docs/roadmap/staged-plan.md` for Stage 3Z and the Stage 4A Discord research-bundle priority.
- Added `stage3z-stage4-discord-bundle-priority` to `data/research/project-direction-change-records-v0.yaml`.
- Updated `ROADMAP.md` so Stage 4A is full Discord research-bundle extraction for Deep Research, with CPU batch API extraction retained later.

## Phase 3 - Documentation Freshness Policy

- Updated `AGENTS.md` for Stage 4A current work, direction-change records, `.md`/`.txt` freshness, and private/generated path documentation.
- Updated `docs/architecture/project-document-freshness-policy.md` with Stage 3Z onboarding maps, a direction-change checklist, and a required doc update matrix.
- Updated `docs/architecture/project-state-and-source-of-truth.md` with onboarding map links and Stage 4A direction.

## Phase 4 - README, Tutorials, And Wiki Source

- Updated README with a "Where To Start" section and Stage 3Z/Stage 4A state.
- Updated tutorials for onboarding links, module maps, local data policy, Discord Stage 4A direction, Codex-assisted development, and troubleshooting.
- Regenerated wiki source with `sync-tutorials-to-wiki.ps1 --DryRun`; serial wiki validation passed.

## Phase 5 - Validation Integration And Focused Tests

- Updated state-drift checks for onboarding docs, Stage 3Y completion, Stage 3Z current/complete state, Stage 4A Discord research-bundle direction, AGENTS freshness policy, and private/generated data map coverage.
- Updated research-synthesis validation for the Stage 4A direction-change record.
- Added Stage 3Z tests for onboarding docs, staged-plan direction, doc freshness policy, wiki validation, and state-drift integration.
- Focused Stage 3Z pytest result: 19 passed.
- Focused ruff result: passed.
- `research-synthesis validate` passed with 6 direction-change records.
- `consistency check-state-drift` passed with 43 checks.

## Phase 6 - Full Validation

- `research-synthesis validate`: passed.
- `research-synthesis summary`: passed with 13 stage summaries, 17 method families, 8 method retirements, 5 Deep Research influence records, and 6 direction-change records.
- `consistency check-state-drift`: passed with 43 checks.
- `consistency check-all --allow-warnings`: passed with 481 checks.
- `libreprimus.cli smoke`: passed.
- Full pytest result: 888 passed.
- Full ruff result: passed.
- `scripts/ci/run-consistency-checks.ps1`: passed.
- `scripts/ci/verify-public-docs-status.ps1`: passed.
- `scripts/ci/verify-lock-hashes.ps1`: passed.
- `scripts/ci/validate-workflow-static.ps1`: passed.
- `scripts/github/validate-wiki-source.ps1`: passed.
- `scripts/github/sync-tutorials-to-wiki.ps1 --DryRun`: passed.
- Raw/generated outputs staged: 0.
- Experiments executed: none.
- Solve claim: none.
