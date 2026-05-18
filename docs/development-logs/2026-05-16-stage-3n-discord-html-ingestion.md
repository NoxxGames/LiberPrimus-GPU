# Stage 3N Discord HTML Ingestion Development Log

Date: 2026-05-16

## Scope

Stage 3N adds admin-approved local Discord HTML archive ingestion as a source-discovery
layer. It is not Discord scraping, live API use, AI summarisation, canonical corpus activation,
or a solve claim.

## Phase 0 Initial State

- Branch: `main`
- Local HEAD: `92a2e407a2b1526a24ff68674b86c999bcf3bb4a`
- `origin/main`: `92a2e407a2b1526a24ff68674b86c999bcf3bb4a`
- Latest known CI: success, run `26005105725`
- Local Discord archive directory: present at `third_party/LiberPrimusDiscordChats`
- Local Discord HTML files: 42
- Estimated archive bytes: 465845099
- Raw Discord files tracked at start: 0
- Generated outputs staged at start: 0
- Raw Discord logs staged at start: 0

## Phase 1 Directories And Ignore Policy

- Added `third_party/LiberPrimusDiscordChats/README.md` and `.gitkeep`.
- Added `data/locks/third-party/discord-chats/`.
- Added `data/observations/discord/`.
- Added generated output directory placeholders under `experiments/results/discord-ingestion/`.
- Updated `.gitignore` so raw Discord HTML logs and generated Discord ingestion outputs remain ignored.

## Phase 2 Schemas

Created seven Stage 3N schemas under `schemas/history/`:

- `discord-archive-record-v0.schema.json`
- `discord-html-file-lock-v0.schema.json`
- `discord-extracted-link-v0.schema.json`
- `discord-attachment-candidate-v0.schema.json`
- `discord-method-claim-candidate-v0.schema.json`
- `discord-numeric-observation-candidate-v0.schema.json`
- `discord-ingestion-summary-v0.schema.json`

The schemas enforce false privacy flags for raw log commits, message body commits, username
commits, AI upload, live API use, and scraping.

## Phase 3 Implementation

Added `python/libreprimus/discord_ingestion/` with:

- local HTML scanning;
- SHA-256 and file-size lock generation;
- href/src and plaintext URL extraction;
- URL classification and Discord attachment query-string redaction;
- attachment candidate extraction without fetching or copying attachments;
- method-claim keyword cluster extraction using redacted summaries only;
- numeric observation extraction using redacted summaries only;
- generated JSONL/JSON exports and a local ignored review index;
- validation and aggregate export helpers.

No live Discord API, scraping, AI upload, OCR, CUDA, or extracted-method execution is used.

## Phase 4 CLI

Added `libreprimus discord-ingest` commands:

- `scan`
- `validate-results`
- `summary`
- `export-aggregate`

The commands support `--allow-missing` so CI and clean workstations do not require local
Discord logs. The generated result files and review index are written only to ignored output
paths.

## Phase 5 Consistency Integration

- Added `python/libreprimus/consistency/check_discord_ingestion.py`.
- Registered the Discord ingestion check group in the consistency runner.
- Updated ignored-output checks for raw Discord HTML logs and generated Stage 3N outputs.
- Updated PowerShell and POSIX consistency scripts with a raw-log-free temp-directory scan.

## Phase 6 Local Discord Ingestion

Ran the scanner against `third_party/LiberPrimusDiscordChats/`.

- HTML files: 42
- Total bytes: 465845099
- Extracted links: 386511
- Unique domains: 2224
- Attachment candidates: 38647
- Method-claim candidates: 48107
- Numeric-observation candidates: 67660
- Known-bogus/debunked or tried-and-failed candidates: 7324
- Warnings: 2

The warnings are high-volume file fragment limits. Generated outputs remain ignored under
`experiments/results/discord-ingestion/stage3n/`.

## Phase 7 Tests

Added Stage 3N tests for schemas, scanner behavior, link extraction, attachment redaction,
claim extraction, numeric extraction, CLI commands, aggregate privacy policy, and ignore policy.

Focused Stage 3N result: `15 passed`.

## Phase 8 Documentation

Added Discord source policy, ingestion, research, and CLI docs. Updated top-level status,
experiment, schema, testing, agent, catalog, roadmap, and tutorial documentation. The docs
reinforce that Discord extraction is reviewable source discovery only and not solve evidence.
