# Status

## Current stage

Stage 3I historical motif Vigenere key-pack execution is complete.

## Completed in Stage 0A

Repository scaffold, documentation, CMake skeleton, optional CUDA smoke scaffold, Python package scaffold, Windows scripts, smoke manifest, and smoke tests.

## Completed in Stage 0B

Non-canonical legacy workbook ingestion support was added for `tranlsations.xlsx`, including raw-workbook ignore safety, lock metadata, Python XLSX parsing, CLI commands, synthetic tests, conditional real-workbook tests, and documentation.

## Completed in Stage 0C

Non-canonical local legacy Pastebin ingestion support was added for `58-Pages-In-Runes-With-Prime-Values-Pastebin.txt`, including raw-source ignore safety, lock metadata, Python TXT parsing, Gematria prime-value validation, CLI commands, synthetic tests, conditional real-source tests, documentation, and developer logs.

## Not yet implemented

No canonical corpus activation, broad unsolved-page campaign, generated result publication, solve claim, or serious CUDA kernel exists yet. Stage 3A/3B add minimal local triage scoring for bounded CPU runs only, Stage 3C calibrates that scorer with small local controls, Stage 3D applies it to a four-key explicit Vigenere preview only, Stage 3E queues the next bounded methods without faking missing executors, Stage 3F runs only the 48-candidate LP evidence-key Vigenere pack, Stage 3G runs only the 256-candidate p56-local prime-minus-one offset sweep, Stage 3H runs only the 64-candidate reset/advance ablation with family-specific negative controls, and Stage 3I runs only the 56-candidate historical motif Vigenere pack.

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

## Completed in Stage 2J

Stage 2J added a standing operator policy for bounded local CPU experiments, bounded experiment queue schemas, policy and queue manifests, a policy checker, generated ignored bounded auto-run records, and `libreprimus bounded-experiment` CLI commands.

The Stage 2J queue includes the first Caesar plus affine reviewable-slice item with candidate upper bound `841`, a solved-baseline regression control, and an intentionally blocked over-budget example. Stage 3A now provides the safe real transform execution/scoring scaffold for the Caesar plus affine item; the solved control passes; the over-budget item is blocked.

Approval workflow remains available as optional/high-risk audit tooling. Policy-passing bounded local CPU items no longer require per-experiment approval. CUDA, cloud, over-budget work, generated-output commits, canonical corpus activation, page-boundary finalization, and solve claims still require explicit instruction or remain blocked.

Developer log: `docs/development-logs/2026-05-16-stage-2j-bounded-auto-run-policy.md`.

## Completed in Stage 3A

Stage 3A added bounded candidate schemas, minimal triage scoring, a tiny committed generic word list, a CPU Caesar plus affine executor, generated ignored candidate output support, `libreprimus bounded-run` CLI commands, and queue-runner integration for the first `841` candidate item.

Local run summary: input slice `stage3a-page-candidate-018-reviewable-slice`, input length `87`, candidate count `841`, Caesar `29`, affine `812`, top observed score `33.353307`, top transform `affine_mod29` with `a=25`, `b=1`.

Generated candidate records, top candidates, run summary, warnings, and result-store preview remain ignored under `experiments/results/bounded-auto-runs/stage3a/`. Minimal triage scores are leads only, not solve evidence. CUDA remains disabled, the canonical corpus remains inactive, page boundaries remain reviewable, and no solve claim is made.

Developer log: `docs/development-logs/2026-05-16-stage-3a-minimal-cpu-caesar-affine-executor.md`.

## Completed in Stage 3B

Stage 3B added candidate-inspection tooling, refined minimal triage scoring, Stage 3A reranking, a Stage 3B bounded queue, and reverse-direction Caesar plus affine execution.

Stage 3A inspection result: original top lead `affine_mod29` with `a=25`, `b=1`, score `33.353307`, qualitative label `weak_noisy`. The top lead had no separator or space context.

Rerank result: refined top lead `affine_mod29` with `a=19`, `b=26`, score `8.040756`, length-normalized score `6.245247`, confidence label `noisy`.

Reverse-direction result: `841` candidates executed; top lead `affine_mod29_reverse` with `a=26`, `a_inverse=19`, `b=20`, score `8.040756`, confidence label `noisy`.

Full candidate dumps remain ignored under `experiments/results/bounded-auto-runs/stage3b/`. Scores and top candidates are leads only, not solve evidence. CUDA remains disabled, the canonical corpus remains inactive, page boundaries remain reviewable, and no solve claim is made.

Developer log: `docs/development-logs/2026-05-16-stage-3b-lead-inspection-scoring-refinement.md`.

## Completed in Stage 3C

Stage 3C added scoring calibration schemas, deterministic null controls, positive controls from solved fixtures and synthetic readable text, negative controls, tiny crib checks, calibrated confidence labels, and `libreprimus scoring` CLI commands.

Calibration result: positive-control length-normalized score range `4.806942` to `29.310739`; null-control range `1.163663` to `11.299382`; negative-control range `-21.268966` to `0.560659`.

Stage 3A original top, Stage 3A refined/reranked top, and Stage 3B reverse-direction top all calibrate as `noisy`. The next bounded method queued is `stage3c-small-vigenere-known-motif-key-list` for Stage 3D.

Generated calibration JSON/JSONL outputs remain ignored under `experiments/results/scoring-calibration/stage3c/`. Crib hits and positive-control-like scores are triage metadata only, not solve evidence. CUDA remains disabled, the canonical corpus remains inactive, page boundaries remain reviewable, and no solve claim is made.

Developer log: `docs/development-logs/2026-05-16-stage-3c-scoring-calibration-null-controls.md`.

## Completed in Stage 3D

Stage 3D added bounded explicit-key Vigenere execution for the Stage 3C-selected small known-motif key-list preview, CLI support, queue-runner integration, tests, documentation, and a summary-only research log.

Local run summary: input slice `stage3a-page-candidate-018-reviewable-slice`, input length `87`, candidate count `4`, keys `LIBER`, `PRIMUS`, `DIVINITY`, `CICADA`.

Top observed key: `LIBER`, total score `6.298395`, length-normalized score `4.753506`, calibrated confidence label `noisy`.

Generated candidate records, calibrated score details, top candidates, warnings, and summary JSON remain ignored under `experiments/results/bounded-auto-runs/stage3d/`. The run is explicit-list only and does not mutate or expand keys. CUDA remains disabled, the canonical corpus remains inactive, page boundaries remain reviewable, and no solve claim is made.

Developer log: `docs/development-logs/2026-05-16-stage-3d-small-vigenere-key-list.md`.

## Completed in Stage 3E

Stage 3E ingested the Deep Research method backlog into committed backlog and bounded queue manifests, added method backlog schemas, deterministic candidate-count validation, dry-run CLI support, executor-support classification, tests, documentation, and summary-only research logs.

Queue summary after Stage 3I: seven Stage 3E items, total deterministic candidate estimate `972`. LP evidence Vigenere pack `48`, p56 local prime-minus-one offsets `256`, historical Vigenere pack `56`, family-specific negative controls `100`, reset/advance ablation `64`, prime mod/gap pack `256`, and future Mersenne/perfect-number probe `192`.

Dry-run result after Stage 3I: all seven items fit the standing operator policy. Four items are runnable now, two are marked `needs_executor`, one is `dry_run_only`, and missing executors are recorded explicitly instead of faking candidate output.

Generated dry-run output remains ignored under `experiments/results/bounded-auto-runs/stage3e/`. CUDA remains disabled, the canonical corpus remains inactive, page boundaries remain reviewable, and no solve claim is made.

Developer log: `docs/development-logs/2026-05-16-stage-3e-method-backlog-ingestion.md`.

## Completed in Stage 3F

Stage 3F implemented `libreprimus bounded-run run-vigenere-key-pack` for the LP evidence-key Vigenere pack and executed `stage3e_vig_lp_evidence_pack_v1`.

Run summary: `48` expected candidates, `48` executed, `0` deferred. The run used 12 declared keys, reset modes `none` and `line`, and advance modes `runes_only` and `token_break_preserving`. The input slice stayed `stage3a-page-candidate-018-reviewable-slice`.

Top lead: key `EMERGE`, reset `none`, advance `runes_only`, score `6.800831`, calibrated label `noisy`. The result is a lead only and not solve evidence.

Generated candidate outputs remain ignored under `experiments/results/bounded-auto-runs/stage3f/`. CUDA remains disabled, the canonical corpus remains inactive, page boundaries remain reviewable, and no solve claim is made.

Developer log: `docs/development-logs/2026-05-16-stage-3f-evidence-key-vigenere-pack.md`.

## Completed in Stage 3G

Stage 3G implemented `libreprimus bounded-run run-prime-offset-sweep` for the p56-local prime-minus-one offset sweep and executed `stage3e_prime_minus_one_offsets_v1`.

Run summary: `256` expected candidates, `256` executed, `0` deferred. The run used offsets `0..63`, directions `forward` and `reverse`, and reset modes `none` and `line`. The input slice stayed `stage3a-page-candidate-018-reviewable-slice`.

Top lead: offset `29`, direction `reverse`, reset `line`, score `1.36709`, calibrated label `inconclusive`. The result is a lead only and not solve evidence.

Stage 3G also added future probe `stage3i_mersenne_prime_stream_tiny_v1` to the backlog and queue with candidate count `192`, implementation status `needs_executor`, and execution disabled for this stage.

Generated candidate outputs remain ignored under `experiments/results/bounded-auto-runs/stage3g/`. CUDA remains disabled, the canonical corpus remains inactive, page boundaries remain reviewable, and no solve claim is made.

Developer log: `docs/development-logs/2026-05-16-stage-3g-p56-local-prime-offset-sweep.md`.

## Completed in Stage 3H

Stage 3H implemented `libreprimus bounded-run run-reset-advance-ablation`, a shared reset/advance state machine, Vigenere and prime-stream adapters, and family-specific negative controls.

Run summary: `64` expected candidates, `64` executed, `0` deferred. The target slice had word, clause, line, and token-break metadata available. Negative controls generated: `100`.

Top lead: base transform `prime_minus_one:offset=1`, reset `line`, advance `runes_only`, score `6.817909`, calibrated confidence `noisy`. The result is a lead only and not solve evidence.

Generated candidate and control outputs remain ignored under `experiments/results/bounded-auto-runs/stage3h/`. CUDA remains disabled, the canonical corpus remains inactive, page boundaries remain reviewable, and no solve claim is made.

Developer log: `docs/development-logs/2026-05-16-stage-3h-reset-advance-ablation.md`.

## Completed in Stage 3I

Stage 3I reused `libreprimus bounded-run run-vigenere-key-pack` for the historical motif Vigenere pack and executed `stage3e_vig_history_key_pack_v1`.

Run summary: `56` expected candidates, `56` executed, `0` deferred. The run used 14 declared historical keys, reset modes `none` and `line`, and advance modes `runes_only` and `token_break_preserving`. The input slice stayed `stage3a-page-candidate-018-reviewable-slice`.

Top lead: key `SELFRELIANCE`, reset `line`, advance `runes_only`, score `6.988031`, calibrated confidence `noisy`. This is slightly above the Stage 3F LP evidence-pack top score but still calibrated noisy and not solve evidence.

Generated candidate outputs remain ignored under `experiments/results/bounded-auto-runs/stage3i/`. CUDA remains disabled, the canonical corpus remains inactive, page boundaries remain reviewable, and no solve claim is made.

Developer log: `docs/development-logs/2026-05-16-stage-3i-historical-motif-vigenere-pack.md`.

## Next prompt recommendation

Stage 3J - implement the tiny Mersenne/perfect-number stream probe or create the visual numeric observation registry. Do not jump to CUDA.
