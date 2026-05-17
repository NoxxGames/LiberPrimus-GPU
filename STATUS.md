# Status

## Current stage

Stage 2I first real bounded CPU exploratory experiment approval packet is complete.

## Completed in Stage 0A

Repository scaffold, documentation, CMake skeleton, optional CUDA smoke scaffold, Python package scaffold, Windows scripts, smoke manifest, and smoke tests.

## Completed in Stage 0B

Non-canonical legacy workbook ingestion support was added for `tranlsations.xlsx`, including raw-workbook ignore safety, lock metadata, Python XLSX parsing, CLI commands, synthetic tests, conditional real-workbook tests, and documentation.

## Completed in Stage 0C

Non-canonical local legacy Pastebin ingestion support was added for `58-Pages-In-Runes-With-Prime-Values-Pastebin.txt`, including raw-source ignore safety, lock metadata, Python TXT parsing, Gematria prime-value validation, CLI commands, synthetic tests, conditional real-source tests, documentation, and developer logs.

## Not yet implemented

No canonical corpus activation, unsolved-page experiment, scoring model, search campaign, generated result publication, or serious CUDA kernel exists yet.

The real workbook was found locally and hash-locked as a raw legacy analysis artefact. It is not committed.

The real local TXT was found locally and hash-locked as a raw legacy LP2 rune/prime-value artefact. It is not committed. Developer log: `docs/development-logs/2026-05-16-stage-0c-legacy-pastebin-ingestion.md`.

## Completed in Stage 0D

The rtkd master transcript was downloaded, ignored, and hash-locked as a proposed primary transcript candidate. The scream314 markdown was downloaded, ignored, and hash-locked as secondary context.

Stage 0D added transcript parsers, signature-based Pastebin alignment, tentative page-boundary candidates, glyph variant `ᛂ` observations, CLI commands, tests, docs, and developer logs.

Real-source smoke summary: rtkd physical lines `931`, Pastebin line pairs `185`, exact matches `1`, high-confidence matches `1`, medium-confidence matches `28`, low-confidence matches `2`, no matches `153`, boundary candidates `74`, glyph variant occurrences `453`.

Developer log: `docs/development-logs/2026-05-16-stage-0d-transcript-alignment-policy.md`.

## Completed in Stage 0D-P

Public-facing tutorials were added under `tutorials/`. GitHub issue templates, issue seed files, label definitions, wiki source pages, and helper scripts were added under `.github/`, `docs/github/`, and `scripts/github/`.

AGENTS.md now documents push, issue idempotency, and wiki mirror policy. Stage 0D-followup remains the next technical stage.

GitHub labels were created or updated and 10 seed issues were opened. Wiki source pages were prepared, but wiki publish failed because the wiki git endpoint was not reachable despite wiki being enabled.

## Toolchain status

Use `scripts/verify-toolchain.ps1` for the current host report. Stage 0A supports CPU-only builds and optional CUDA smoke builds.

## Completed in Stage 0D-followup

Stage 0D-followup added transcript logical-line and rune-stream views, bounded stream-subsequence alignment, alignment-gap diagnostics, and stricter page-boundary confidence auditing.

Real-source follow-up summary: rtkd physical lines `931`, logical lines `798`, Pastebin line pairs `185`, exact matches `52`, high-confidence matches `129`, medium-confidence matches `0`, low-confidence matches `2`, no matches `2`, no-match reduction `151`, boundary candidates `74`, high/medium/low/none boundaries `50/3/21/0`, overgeneration warning `true`.

Remaining gaps: two no-match records and two low-confidence records still require review. Boundary candidates remain tentative and non-canonical.

Developer log: `docs/development-logs/2026-05-16-stage-0d-followup-alignment-gap-audit.md`.

## Completed in Stage 0E

Stage 0E added frozen tooling profiles, corpus schemas, and an rtkd master corpus v0 candidate generator.

Profile hashes: Gematria `80cb10863b1fd3de57b44000c6bd90c307f11b90cc9d864a3d493e3f069c3280`; glyph variants `df81597b15c991ddf2894a44f1a6980554a5e463881d00a31524e5366dd704bf`; separator grammar `e0a5f682ced4afcf25956d06b1b49d1356203fe8ed47c7dec41365e3bec7b8e7`.

Real-source candidate summary: physical lines `931`, logical lines `1729`, tokens `22382`, rune tokens `15933`, separator tokens `5795`, page candidates `74`, warnings `311`, `canonical_corpus_active=false`.

Developer log: `docs/development-logs/2026-05-16-stage-0e-gematria-separators-corpus-candidate.md`.

## Completed in Stage 1A

Stage 1A added solved-page golden fixture schemas, direct-translation fixture manifests, a direct-translation decoder, span selectors, reproduction CLI commands, tests, docs, and developer logs.

Real-source fixture summary: fixtures `4`, pass/fail/pending/skipped `4/0/0/0`, direct translation implemented `true`, `canonical_corpus_active=false`.

Developer log: `docs/development-logs/2026-05-16-stage-1a-direct-translation-golden-fixtures.md`.

## Completed in Stage 1B

Stage 1B added CPU-only reverse Gematria and rotated reverse Gematria fixture reproduction.

Real-source fixture summary: Atbash-family fixtures `3`, pass/fail/pending/skipped `3/0/0/0`, direct regression `4/0/0/0`, `canonical_corpus_active=false`.

Implemented fixture methods: `reverse_gematria` and `rotated_reverse_gematria`. Vigenere, prime streams, generic affine search, scoring, and CUDA remain unimplemented.

Developer log: `docs/development-logs/2026-05-16-stage-1b-atbash-family-golden-fixtures.md`.

## Completed in Stage 1C

Stage 1C mirrored and locked additional reference-source files, added CPU-only explicit-key Vigenere fixture reproduction, and added Vigenere known-solved fixtures.

Reference mirror summary: files attempted `9`, locked `9`, failed `0`; scream314 method notes `10`; lipeeeee tooling notes `32`.

Real-source fixture summary: Vigenere fixtures `2`, pass/fail/pending/skipped `2/0/0/0`, direct regression `4/0/0/0`, Atbash regression `3/0/0/0`, `canonical_corpus_active=false`.

Implemented fixture method: `vigenere_explicit_key`. Key search, p56 prime streams, generic affine/shift search, scoring, and CUDA remain unimplemented.

Developer log: `docs/development-logs/2026-05-16-stage-1c-vigenere-golden-fixtures.md`.

## Completed in Stage 1D

Stage 1D added CPU-only p56 prime-minus-one / phi-prime known-solved fixture reproduction and payload preservation checks.

Real-source fixture summary: prime-stream fixtures `1`, pass/fail/pending/skipped `1/0/0/0`, direct regression `4/0/0/0`, Atbash regression `3/0/0/0`, Vigenere regression `2/0/0/0`, `canonical_corpus_active=false`.

Payload check result: p56 hex block `pass`.

Implemented fixture method: `prime_minus_one_stream`, with `phi_prime_stream` as an equivalent alias for prime inputs. Generic prime-stream search, affine/shift search, scoring, and CUDA remain unimplemented.

Developer log: `docs/development-logs/2026-05-16-stage-1d-p56-prime-stream-golden-fixture.md`.

## Completed in Stage 2A

Stage 2A added the CPU reference transform registry and manifest-addressable solved-baseline runner.

Registry summary: `cpu-reference-transforms-v0`, transforms `6`, alias entries `1`, `search_enabled=false`, `cuda_enabled=false`, `scoring_enabled=false`.

Solved-baseline manifest summary: manifests `5`, all-known fixture groups `4`, pass/fail/pending/skipped `10/0/0/0`. Direct translation pass count `4`, Atbash-family pass count `3`, Vigenere pass count `2`, prime-stream pass count `1`.

Generated manifest-runner outputs remain ignored under `experiments/results/solved-baselines/stage2a/`. `canonical_corpus_active=false` and `page_boundaries_final=false`.

Developer log: `docs/development-logs/2026-05-16-stage-2a-cpu-transform-registry.md`.

## Completed in Stage 2B

Stage 2B added the experiment result-store foundation for solved-baseline regression imports.

Result-store summary: schemas `6`, JSONL sink `implemented`, SQLite sink `implemented`, provenance capture `implemented`, solved-baseline import `implemented`, generated outputs ignored under `experiments/results/result-store/stage2b/`.

Imported solved-baseline run summary: pass/fail/pending/skipped `10/0/0/0`, search/cuda/scoring `false/false/false`, `canonical_corpus_active=false`, `page_boundaries_final=false`.

Developer log: `docs/development-logs/2026-05-16-stage-2b-result-store-foundation.md`.

## Completed in Stage 2C

Stage 2C added GitHub Actions CI and local reproduction scripts.

CI summary: workflow `.github/workflows/ci.yml`, Python 3.12 job with Ruff, pytest, Python smoke, transform-registry validation, solved-baseline manifest validation, and result-store manifest validation. CPU-only CMake smoke job is included with `LPGPU_ENABLE_CUDA=OFF`.

Policy summary: CI is raw-data-free, CUDA-free, secret-free, and does not upload generated corpus or result artifacts by default.

Stage 2C-followup reformatted the workflow into readable multi-line YAML, added static YAML parsing and formatting checks, and added local workflow validation scripts.

Stage 2C-followup-4 updated public README/STATUS/ROADMAP stage status and added tests that prevent stale top-level public status and next-milestone text.

Developer log: `docs/development-logs/2026-05-16-stage-2c-github-actions-ci.md`.

Follow-up developer log: `docs/development-logs/2026-05-16-stage-2c-followup-ci-hardening.md`.

## Completed in Stage 2D

Stage 2D added raw-data-free consistency checks for registry metadata, solved-baseline manifests, result-store manifests, schemas, public documentation status, ignored-output policy, and result-store records when generated outputs are present.

CI now runs the Stage 2D consistency suite without raw data, search, scoring, CUDA, secrets, or generated artifact uploads.

Developer log: `docs/development-logs/2026-05-16-stage-2d-schema-docs-result-hardening.md`.

## Completed in Stage 2E

Stage 2E added exploratory experiment schemas, dry-run-only manifests, candidate-count estimators, safety gates, generated dry-run plan outputs, and `libreprimus experiment` CLI commands.

Dry-run summary: direct `1`, Caesar preview `29`, affine mod-29 preview `812`, Vigenere key-list preview `2`, prime-stream parameter preview `1`. Execution, search, candidate generation, scoring, CUDA, canonical corpus activation, and page-boundary finalization remain disabled.

Developer log: `docs/development-logs/2026-05-16-stage-2e-cpu-exploratory-dry-run-planner.md`.

## Completed in Stage 2F

Stage 2F added CPU execution schemas, safe synthetic execution manifests, a solved-fixture replay manifest, a blocked unsolved negative manifest, safety gates, generated execution output support, and `libreprimus execution` CLI commands.

Execution is restricted to synthetic and solved-fixture-only scopes. Unsolved-page execution, search, candidate generation, scoring, CUDA, canonical corpus activation, and page-boundary finalization remain prohibited.

Developer log: `docs/development-logs/2026-05-16-stage-2f-bounded-cpu-execution-harness.md`.

## Completed in Stage 2G

Stage 2G added experiment proposal schemas, review checklist schemas, approval record schemas, review packet schemas, proposal examples, pending/denied approval examples, approval-gate logic, generated review packets, and `libreprimus proposal` CLI commands.

All committed Stage 2G proposals are blocked pending explicit human approval. No proposal executes, no candidate plaintexts are generated, and search, scoring, CUDA, canonical corpus activation, and page-boundary finalization remain prohibited.

Developer log: `docs/development-logs/2026-05-16-stage-2g-experiment-proposal-approval-workflow.md`.

## Completed in Stage 2H

Stage 2H added approval-gated execution request, plan, and result schemas; safe approved synthetic and solved-control proposal records; scope-bound approval records; blocked no-op real-proposal handling; an approval execution bridge; and `libreprimus approval-execution` CLI commands.

Approved control execution is limited to `synthetic_only` and `solved_fixture_only` requests. Real unsolved-page proposals remain blocked, no approved unsolved-page approval records are committed, and search, candidate generation, scoring, CUDA, canonical corpus activation, and page-boundary finalization remain disabled.

Developer log: `docs/development-logs/2026-05-16-stage-2h-approval-gated-execution.md`.

## Completed in Stage 2I

Stage 2I added the first real bounded CPU exploratory proposal packet for `stage2i-first-bounded-caesar-affine-review`, an approval-readiness schema, a pending approval record, readiness analysis, generated ignored readiness packets, and `libreprimus approval-readiness` CLI commands.

The proposal touches reviewable unsolved metadata only and includes no raw unsolved text. Candidate-count preview is Caesar `29` plus affine mod-29 `812`, for total upper bound `841`. Approval remains pending, `approved_for_execution=false`, and execution/search/candidate-generation/scoring/CUDA remain disabled.

Developer log: `docs/development-logs/2026-05-16-stage-2i-first-real-proposal-packet.md`.

## Next prompt recommendation

Stage 2J - human decision step: approve, deny, or revise the first bounded CPU exploratory experiment proposal. Do not execute unless an explicit approved approval record is supplied.
