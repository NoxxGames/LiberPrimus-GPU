# Stage 3O Discord Source Promotion And Wiki Development Log

Date: 2026-05-16

## Scope

Stage 3O promotes selected public, redacted Discord-discovered source links and observation
candidates into committed review records, expands public tutorials, generates GitHub Wiki source
pages from tutorials, and adds Wiki sync scripts.

The stage does not publish raw Discord logs, use Discord APIs, scrape Discord, execute extracted
methods, use CUDA, activate the canonical corpus, finalize page boundaries, or claim a solve.

## Phase 0 Initial State

- Branch: `main`
- Local HEAD: `21d890b761e809f43f749fe93a8be2a4a6294bf0`
- `origin/main`: `21d890b761e809f43f749fe93a8be2a4a6294bf0`
- Latest known CI: success, run `26006803436`
- Stage 3N generated outputs: present
- Discord aggregate records: present
- Local Discord raw dir: present
- Tutorial files: 13
- GitHub CLI authenticated: true
- Repo Wiki enabled: true
- Wiki remote accessible: false, repository not found
- Generated outputs staged: 0
- Raw Discord logs staged: 0

## Phase 1 Output And Ignore Policy

- Added ignored generated output areas for Discord promotion and Wiki sync.
- Added `.wiki-worktree/` ignore rules.
- Preserved raw Discord HTML ignore rules.

## Phase 2 Discord Promotion

- Added `python/libreprimus/discord_promotion/`.
- Added ranking, redaction, export, summary, and validation helpers.
- Promoted `500` public source links, `200` method-claim candidates, and `200` numeric-observation candidates.
- Rejected `362666` private or unsafe links.
- Committed promotion records are redacted and review-only.

## Phase 3 Discord Promotion CLI

- Added `libreprimus discord-promote promote`.
- Added `libreprimus discord-promote validate-promoted`.
- Added `libreprimus discord-promote summary`.
- Validation confirms no raw message bodies, usernames, private Discord attachment URLs, or solve claims in promoted records.

## Phase 4 README And Tutorials

- Updated `README.md` with a public "How To Use This Repo" path.
- Expanded `tutorials/` with current setup, policy, testing, bounded experiment, image-analysis, Discord ingestion, source registry, Wiki mirror, Codex, and troubleshooting guides.

## Phase 5 Wiki Source

- Added Wiki source generation under `docs/wiki-source/`.
- Added `Home.md`, `_Sidebar.md`, and `28` mirrored tutorial pages.
- Added Wiki sync and validation scripts for PowerShell and shell.
- Dry-run and validation passed locally.

## Phase 7 Consistency Integration

- Added Stage 3O Discord promotion consistency checks.
- Added Wiki source validation to local CI scripts.
- Added Stage 3O ignore-policy checks for generated outputs and Wiki worktrees.
- Local consistency check passed with `356` checks.

## Phase 8 Local Run

- Re-ran `libreprimus discord-promote promote`.
- Promoted public links: `500`.
- Promoted method claims: `200`.
- Promoted numeric observations: `200`.
- Rejected private or unsafe links: `362666`.
- Wiki source pages: `30`.
- Wiki dry-run passed: true.
- Generated outputs staged: `0`.
- Raw Discord logs staged: `0`.

## Phase 9 Tests

- Added Stage 3O tests for promotion, privacy, tutorial docs, Wiki source, Wiki scripts, and ignore policy.
- Ruff passed for `python/libreprimus` and `tests/python`.
- Pytest passed: `719 passed`.

## Phase 11 Validation

- `libreprimus.cli smoke`: passed.
- `libreprimus.cli consistency check-all --allow-warnings`: `356` passed.
- `scripts/ci/run-consistency-checks.ps1`: passed.
- `scripts/ci/verify-public-docs-status.ps1`: passed.
- `scripts/ci/verify-lock-hashes.ps1`: passed.
- `scripts/ci/validate-workflow-static.ps1`: passed.
- `scripts/github/validate-wiki-source.ps1`: passed.
- `scripts/github/sync-tutorials-to-wiki.ps1 --DryRun`: passed.
