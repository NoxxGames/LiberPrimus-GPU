# Stage 3R Discord Lead Promotion Audit Development Log

Date: 2026-05-16

## Scope

Stage 3R audits redacted Stage 3Q Discord-derived leads, promotes only corroborated public-source and exact-observation candidates, preserves known false-positive classes as negative controls, and creates the first disabled post-Discord experiment manifests.

The stage does not publish raw Discord logs, commit message bodies or usernames, call Discord APIs, scrape Discord, execute the new experiments, use CUDA, activate canonical corpus, finalize page boundaries, or claim a solve.

## Phase 0 Initial State

- Branch: `main`
- Local HEAD: `6862962472bc48df3e5ff28f312024fb939fafa4`
- `origin/main`: `6862962472bc48df3e5ff28f312024fb939fafa4`
- Latest CI: success, run `26011781351`
- Stage 3Q generated outputs present: true
- Stage 3O promoted records present: true
- Source registry present: true
- Visual observations present: true
- Cookie records present: true
- Lead-triage report present: true
- Generated outputs staged: `0`
- Raw Discord logs staged: `0`
- Raw images staged: `0`
- Root reports staged: `0`

## Phase 1 Output And Manifest Directories

- Added generated output area under `experiments/results/discord-lead-promotion/stage3r/`.
- Added post-Discord manifest directory under `experiments/manifests/post-discord/`.
- Added ignore policy for generated Stage 3R promotion audit outputs.
- Preserved raw Discord and raw page-image ignore rules.

## Phase 2 Schemas

- Added promoted Discord source, promoted Discord observation, negative-control, post-Discord experiment manifest, and GP/rune claim schemas.
- Schemas require false privacy flags for raw messages, usernames, private URLs, and canonical trust.
- Post-Discord manifest schema requires `execution_enabled=false`, `cuda_enabled=false`, `no_solve_claim=true`, `canonical_corpus_active=false`, and `page_boundaries_final=false`.

## Phase 3 Implementation

- Added `python/libreprimus/discord_lead_promotion/` with loaders, public URL corroboration helpers, curated promotion records, negative controls, disabled manifest builders, summary loading, export helpers, and validation.
- The runner reads Stage 3Q generated indexes when present and falls back to Stage 3O committed promotions if generated coverage is reduced.
- Generated audit records are written only under `experiments/results/discord-lead-promotion/stage3r/`.
- Committed outputs are restricted to curated YAML records and disabled manifest YAML.
- Privacy flags remain false for raw messages, usernames, and private URLs.

## Phase 4 CLI

- Added `libreprimus discord-leads promote`.
- Added `libreprimus discord-leads build-manifests`.
- Added `libreprimus discord-leads validate`.
- Added `libreprimus discord-leads summary`.
- The command group supports missing generated Stage 3Q inputs for raw-log-free CI behavior.

## Phase 5 Local Run

- Ran Stage 3R promotion against local Stage 3Q outputs.
- Promoted source records: 13.
- Promoted observation records: 11.
- Negative controls: 11.
- Duplicate existing source references counted: 3.
- Unsafe/private or quarantined records counted: 25.
- Created three disabled post-Discord manifests:
  - `EXP-3R-001` with candidate cap 576.
  - `EXP-3R-003` with candidate cap 144.
  - `EXP-3R-004` with claim cap 64.
- Validation passed for promoted records and disabled manifests.
- No experiments were executed.

## Phase 6 Tests

- Added Stage 3R tests for schemas, URL corroboration, promotion behavior, negative controls, manifest building, CLI behavior, privacy policy, and ignore policy.
- Focused Stage 3R pytest run passed: `13 passed, 752 deselected`.
- Focused ruff check passed for Stage 3R package and tests.

## Phase 7 Consistency Integration

- Added Stage 3R consistency checks for promoted records, negative controls, disabled manifests, ignored generated audit outputs, raw Discord log ignores, and raw page-image ignores.
- Updated the consistency runner with the `discord_leads` group.
- Updated local CI scripts to validate Stage 3R records and manifests without requiring real Discord logs or generated Stage 3Q outputs.

## Phase 8 Documentation, Tutorials, And Wiki Source

- Added Stage 3R history, experiment, research, and CLI reference documentation.
- Added summary-only Stage 3R research logs.
- Copied the local Discord bundle lead-triage report into `docs/research/` with a source-corroboration and no-solve-claim note.
- Updated README, STATUS, ROADMAP, EXPERIMENTS, RESULTS_SCHEMA, TESTING, AGENTS, CIPHER_CATALOG, and relevant tutorials.
- Regenerated Wiki source from tutorials and validated it locally.
