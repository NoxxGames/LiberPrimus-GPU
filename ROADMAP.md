# Roadmap

## Current Direction

Current completed stage: Stage 6E - Readiness consolidation, bridge source-locks, hook/doc-staleness repair, and Stage 6F manifest inputs, without execution.

Next routed stage: Stage 6F - Final finite Stage 7 probe manifest and archive-run contract, without execution.

Stage 6D is a source-lock and automation/hook triage insertion only. It preserves canonical doublet boundary profiles as bounded metadata reproduction and routes final finite Stage 7 manifest and archive-run contract work to Stage 6E. Stage 7 execution, Stage 8 triangle readiness, and Stage 9 experiments remain blocked.

The durable staged plan is maintained at [`docs/roadmap/staged-plan.md`](docs/roadmap/staged-plan.md). Update that file whenever stage status, direction, experiment priority, or method-family retirement/reopening changes.

## Phase 0A - Project bootstrap

Create repository structure, documentation, toolchain scripts, C++ smoke build, optional CUDA smoke build, Python package, and smoke tests.

## Phase 0B - Source mirroring and corpus locks

Mirror source archives, pin SHA-256 locks, define canonical transcript/versioning policy, and freeze Gematria profile metadata without cryptanalysis.

Stage 0B legacy workbook ingestion is completed as a separate non-canonical legacy-source step. Canonical corpus mirroring remains future work.

## Phase 0C - Source archive mirroring, transcript locks, and Gematria profile freeze

Mirror primary source archives, pin SHA-256 locks, define canonical transcript/versioning policy, and freeze Gematria profile metadata without implementing unsolved-page cryptanalysis.

Stage 0C local legacy Pastebin ingestion is completed as a separate non-canonical legacy-source step.

## Phase 0D - Align legacy Pastebin line-pairs

Align legacy Pastebin line-pairs with primary transcript/page-image sources and infer tentative page boundaries with confidence labels.

Stage 0D transcript alignment and policy scaffolding is completed, with significant unmatched regions documented.

## Phase 0D-P - Public docs, wiki, and issue bootstrap

Add public tutorials, GitHub issue templates, issue seeds, wiki source pages, project-management scripts, and push workflow documentation.

## Phase 0D-followup - Resolve transcript-alignment gaps

Resolve transcript-alignment gaps, ambiguous page-boundary candidates, and glyph-variant evidence before corpus freeze.

Stage 0D-followup added transcript views, bounded stream-subsequence matching, gap diagnostics, and boundary confidence auditing. It reduced real-source no-match records from `153` to `2`, but two low-confidence records and boundary overgeneration still require human review.

## Phase 0D-followup-2 - Inspect remaining unmatched spans, if needed

If the remaining ambiguous records block corpus policy work, manually inspect unmatched spans, compare alternate transcript segmentation, and decide whether rtkd logical views or Pastebin source structure should drive LP2 alignment.

## Phase 0E - Freeze Gematria profile and separator grammar

Freeze Gematria profile and separator grammar, then create canonical corpus v0 candidate records with page-boundary candidates preserved as non-final metadata.

Stage 0E generated frozen Gematria, separator, and glyph variant profiles plus an inactive rtkd master v0 corpus candidate.

## Phase 1A - Solved-page golden fixture framework

Implement solved-page golden fixture framework and reproduce direct-translation solved pages using Stage 0E profiles and corpus candidate records. Do not add brute-force search.

Stage 1A added direct-translation solved fixtures for four known direct sections and a reproduction CLI. Generated solved-baseline outputs remain ignored.

## Phase 1B - Reverse Gematria / Atbash-family reproduction

Reproduce clearly documented reverse Gematria or Atbash-family solved pages using the Stage 1A fixture framework. Do not add brute-force search.

Stage 1B added reverse Gematria and rotated reverse Gematria known-solved fixtures. The direct fixture regression still passes.

## Phase 1C - Explicit-key Vigenere solved-page reproduction

Reproduce documented Vigenere solved pages with explicit locked-source keys and skip rules only where the locked references support them. Do not add key search.

Stage 1C added reference-source locks and explicit-key Vigenere solved fixtures for `DIVINITY` and `FIRFUMFERENFE`. Direct and Atbash-family regressions still pass. No key search was added.

## Phase 1D - p56 prime-minus-one / phi-prime reproduction

Reproduce p56 An End only if locked references and fixture spans support the prime-minus-one / phi-prime method. Preserve payload checks and do not add search.

Stage 1D added a p56 prime-minus-one known-solved fixture with a passing payload hash check. Direct, Atbash-family, and Vigenere regressions still pass. No prime-stream search was added.

## Phase 2A - CPU transform registry foundation

Register solved-baseline CPU reference transforms for manifest-addressable runs: direct translation, reverse Gematria, rotated reverse Gematria, explicit-key Vigenere, and prime-minus-one. Do not start search campaigns yet.

Stage 2A added `cpu-reference-transforms-v0`, registry dispatch, solved-baseline run manifests, and an all-known solved-baseline runner with 10 passing known fixtures. Search, scoring, CUDA, canonical corpus activation, and page-boundary finalization remain disabled.

## Phase 2B - Experiment result store and run-record foundation

Add durable JSONL/SQLite result sinks, run-record schemas, manifest provenance, solved-baseline result import, and validation before unsolved-page search campaigns begin.

Stage 2B added result-store schemas, JSONL and SQLite sinks, provenance capture, a solved-baseline import manifest, result-store CLI commands, and generated result-store validation. It imports the Stage 2A all-known solved-baseline run with pass/fail/pending/skipped `10/0/0/0`. Search, scoring, CUDA, canonical corpus activation, and page-boundary finalization remain disabled.

## Phase 2C - CI and safe experiment scaffolding

Add GitHub Actions CI for Python tests, ruff, schema validation, and CPU-only smoke commands, or add bounded CPU experiment-manifest scaffolding only after result-store validation. Do not jump directly to CUDA or unsolved-page search.

Stage 2C added GitHub Actions CI and local CI reproduction scripts. The workflow runs raw-data-free Python checks, schema/manifest validation, and a CPU-only CMake smoke job with CUDA disabled. It does not upload generated artifacts or run search/scoring.

Stage 2C-followup hardened the workflow with readable multi-line YAML, static YAML structure checks, and local workflow validation scripts.

Stage 2C-followup-2 added post-push raw GitHub workflow verification scripts and `gh` PATH troubleshooting while keeping the workflow raw-data-free, CUDA-free, secret-free, and artifact-upload-free by default.

Stage 2C-followup-3 repaired Git attributes, normalized canonical profile/registry JSON locks to LF bytes, and added lock-hash verification to prevent Windows/Linux SHA drift.

Stage 2C-followup-4 updated public README/STATUS/ROADMAP status text and added CI-covered tests to prevent stale top-level public status and next-milestone drift.

Stage 2C-followup-5 added remote Git blob verification for the CI workflow and `.gitattributes`, documenting that fetched Git blobs and GitHub API contents outrank potentially cached raw URL views.

## Stage 2D - CI-gated schema and docs hardening

Add schema/docs consistency checks and harden manifest/result-store validation before first bounded CPU exploratory experiment scaffolding.

Stage 2D added a raw-data-free consistency package, CLI commands, CI scripts, workflow gates, and tests covering registry, manifest, schema, docs, ignored-output, and result-store consistency.

## Stage 2E - CPU experiment manifest scaffold and dry-run planner

Design CPU exploratory experiment manifests and a dry-run planner for bounded baseline transforms without executing unsolved-page search campaigns.

Stage 2E added exploratory schemas, dry-run-only manifests, candidate-count estimators, safety gates, generated dry-run plan output support, CLI commands, CI consistency integration, and documentation. No search, scoring, CUDA, candidate generation, canonical corpus activation, or page-boundary finalization was added.

## Stage 2F - Synthetic and solved-fixture CPU execution harness design

Design a bounded CPU experiment execution harness for synthetic and solved-fixture-only runs. Keep unsolved-page campaigns out of scope until dry-run gates, result-store policy, and review criteria remain stable.

Stage 2F added CPU execution schemas, synthetic and solved-fixture-only manifests, a blocked unsolved negative manifest, safety gates, `libreprimus execution` CLI commands, generated ignored execution outputs, tests, and documentation. It does not authorize unsolved-page execution, search, scoring, CUDA, canonical corpus activation, or page-boundary finalization.

## Stage 2G - First bounded CPU exploratory experiment proposal and approval workflow

Prepare the first bounded CPU exploratory experiment proposal and approval workflow. Real unsolved-page execution still requires explicit human approval, pinned manifests, result-store policy, stop conditions, and review criteria before any run.

Stage 2G added proposal schemas, approval record schemas, review checklists, blocked proposal examples, pending/denied approval examples, review packet generation, `libreprimus proposal` CLI commands, tests, and documentation. It does not approve or execute proposals and does not start real unsolved-page search.

## Stage 2H - Approval-gated execution path

Implement an approval-gated execution path for approved proposals, initially limited to synthetic/solved controls or a no-op real proposal. Do not jump directly to broad unsolved search, scoring campaigns, or CUDA.

Stage 2H added approval-gated execution request, plan, and result schemas, approved synthetic and solved-control approval examples, blocked no-op real-proposal handling, `libreprimus approval-execution` CLI commands, tests, and documentation. It does not approve real unsolved-page execution and does not start search, candidate generation, scoring, CUDA, canonical corpus activation, or page-boundary finalization.

## Stage 2I - First real bounded CPU exploratory approval packet

Prepare and review the first real bounded CPU exploratory experiment approval packet. Do not execute it unless explicit human approval is supplied in a separate future step, and do not broaden into search campaigns or CUDA.

Stage 2I added `stage2i-first-bounded-caesar-affine-review`, a pending approval record, an approval-readiness packet schema, readiness analyzer, `libreprimus approval-readiness` CLI commands, tests, and documentation. It records a Caesar plus affine mod-29 preview upper bound of `841`, commits no approved real-unsolved approval records, does not execute, and does not generate candidates, score output, use CUDA, activate the canonical corpus, or finalize page boundaries.

## Stage 2J - Standing bounded auto-run policy

Replace per-experiment approval as the default path with a standing bounded local CPU operator policy. Keep approval tooling as optional/high-risk audit tooling for out-of-policy work.

Stage 2J added `operator-policy-v0`, bounded queue schemas, `experiments/policies/operator-policy-v0.yaml`, `experiments/queues/stage2j-bounded-cpu-queue.yaml`, a policy checker, generated ignored bounded auto-run records, and `libreprimus bounded-experiment` CLI commands. The `841` candidate Caesar plus affine reviewable-slice item is policy-eligible, the solved-baseline control passes, and the over-budget negative example is blocked.

## Stage 3A - Minimal real bounded CPU execution/scoring scaffold

Implement the minimal safe executor needed for the `841` candidate Caesar plus affine queue item. Keep CUDA, broad brute force, cloud, canonical corpus activation, page-boundary finalization, generated-output commits, and solve claims out of scope.

Stage 3A added bounded candidate output schemas, minimal deterministic triage scoring, a CPU Caesar plus affine executor, `libreprimus bounded-run` CLI commands, and queue-runner integration. The first bounded run generated `841` ignored candidate records for one reviewable slice and made no solve claim.

## Stage 3B - Inspect bounded leads and refine next queue item

Inspect Stage 3A top candidates as leads, add null-control expectations, and queue the next bounded method or scoring refinement. Do not escalate to broad campaigns, CUDA, canonical corpus activation, page-boundary finalization, or solve claims.

Stage 3B added candidate inspection, refined scoring, reranking, a Stage 3B bounded queue, and a reverse-direction Caesar plus affine comparison. Results remain noisy and no solve claim is made.

## Stage 3C - Scoring calibration and null controls

Improve score calibration with null controls, crib/phrase sanity checks, and clearer lead review thresholds before widening transform families. Do not jump directly to CUDA or broad unsolved search.

Stage 3C added positive controls, deterministic null controls, negative controls, tiny crib checks, calibrated labels, `libreprimus scoring` CLI commands, and `experiments/queues/stage3c-bounded-cpu-queue.yaml`. Stage 3A/3B top leads remain noisy; no solve claim is made.

## Stage 3D - Small Vigenere known-motif key-list preview

Run the conservative Stage 3C-selected bounded CPU method with calibrated scoring. Keep the explicit key list tiny, generated outputs ignored, no CUDA, no broad key search, no canonical corpus activation, no page-boundary finalization, and no solve claim.

Stage 3D added bounded explicit-key Vigenere execution for exactly `LIBER`, `PRIMUS`, `DIVINITY`, and `CICADA`. The run produced four ignored candidates; top key `LIBER` calibrated as `noisy`, so no solve claim is made.

## Stage 3E - Method prioritization backlog

If Stage 3D remains noisy, use Deep Research or a similarly bounded planning pass to prioritize the next conservative CPU method family. Do not jump directly to CUDA, broad Vigenere search, canonical corpus activation, page-boundary finalization, generated-output publication, or solve claims.

Stage 3E ingested the Deep Research method backlog, added machine-readable backlog and bounded queue manifests, validated deterministic candidate counts, and dry-ran policy-fitting queue items. Stage 3G later adds the future Mersenne/perfect-number probe to the same queue. Missing executors remain marked explicitly instead of faked.

## Stage 3F - Evidence-key Vigenere pack executor

Stage 3F implements the reset/advance-aware explicit-key Vigenere pack executor for `stage3e_vig_lp_evidence_pack_v1` and runs that one bounded LP evidence pack. It keeps the key list manifest-bound, CPU-only, generated outputs ignored, and no solve claim.

The Stage 3F result remains noisy, so do not widen Vigenere keys or jump to CUDA.

## Stage 3G - p56-local prime-minus-one offset sweep

Implement the p56-local prime-minus-one offset sweep executor for `stage3e_prime_minus_one_offsets_v1` if it still fits the standing operator policy. Keep offsets, directions, and reset modes manifest-bound, CPU-only, generated outputs ignored, and no solve claim.

Stage 3G implements the p56-local prime-minus-one offset sweep and runs all `256` bounded candidates. The top lead is `inconclusive`, not solve evidence. Stage 3G also queues a future `192` candidate Mersenne/perfect-number probe without executing it.

## Stage 3H - Reset/advance ablation or family-specific negative controls

If Stage 3G remains inconclusive or noisy, implement reset/advance ablation or family-specific negative controls before widening stream families. Keep candidate counts bounded, generated outputs ignored, and no solve claim.

Stage 3H implements a shared reset/advance state machine, Vigenere and prime-stream adapters, and family-specific negative controls. It runs all `64` bounded ablation candidates, generates `100` ignored controls, keeps unsupported metadata modes deferrable, and makes no solve claim.

## Stage 3I - Mersenne tiny probe or historical Vigenere follow-up

Run a bounded historical Vigenere pack follow-up using the reset/advance executor, or defer to the queued tiny Mersenne/perfect-number stream probe if selected. Keep candidate counts bounded, generated outputs ignored, and no solve claim. Do not jump to CUDA.

Stage 3I runs the bounded historical motif Vigenere pack for `stage3e_vig_history_key_pack_v1`: 14 manifest-bound keys, two reset modes, two advance modes, and `56` candidates. The top lead remains calibrated `noisy`, so it is not solve evidence and does not justify widening into dictionary search.

## Stage 3J - Mersenne/perfect-number tiny stream probe

If Stage 3I remains noisy, implement the queued tiny Mersenne/perfect-number stream probe. Keep the finite exponent sequence fixed, report duplicate stream signatures, keep generated outputs ignored, and do not jump to CUDA.

Stage 3J implements and runs the `192` candidate Mersenne/perfect-number tiny stream probe. The top lead remains calibrated `inconclusive` with a raw `garbage` triage label, so it is not solve evidence and does not justify broadening into arbitrary number-sequence search.

## Stage 3K - Visual numeric observation registry or archive-image source audit

If Stage 3J remains inconclusive or noisy, create a reviewable visual numeric observation registry or archive-image source audit. Visual observations such as base-60 or cuneiform-like numbers, binary dot patterns, symmetry/asymmetry, and page imagery must be captured as reviewable observations before being promoted into bounded experiment seeds. Do not jump to CUDA.

Stage 3K adds source/archive classification, local image lock records, deterministic image metadata extraction, reviewable visual numeric observations, cookie/hash records, schemas, CLI validation, tests, and documentation. It does not execute image-derived text experiments and makes no solve claim.

## Stage 3L - Bounded cookie-hash preimage packs

Stage 3L runs explicit SHA-256-only literal and numeric/base29 candidate packs against the archived 2013 `167` and `761` cookie/hash artefacts. It found zero exact matches, made no fuzzy or partial-match claims, and made no solve claim.

## Stage 3M - Deterministic image/audio/web analysis CLIs or Onion7 numeric seed registry

Stage 3M adds deterministic local Liber Primus page-image analysis CLIs and visual-feature summaries. It records grayscale statistics, threshold summaries, 4-connected component summaries, symmetry metrics, bit-plane densities, and review-only feature candidates. Generated outputs remain ignored, no OCR or AI/ML interpretation is used, and no image-derived search or solve claim is made.

## Stage 3N - Admin-approved Discord HTML archive ingestion

Stage 3N adds privacy-preserving ingestion for admin-provided local Discord HTML exports. It scans local ignored HTML logs, extracts redacted source-discovery links, attachment candidates, method-claim candidates, and numeric-observation candidates, and commits aggregate summaries only. Raw Discord logs, message bodies, usernames, private attachment URLs, and generated review indexes remain uncommitted.

## Stage 3O - Review extracted Discord source links

Stage 3O promotes a bounded public-safe subset of Stage 3N Discord source-discovery output into redacted review records, expands public tutorials, and generates GitHub Wiki mirror source pages. Raw Discord logs, message bodies, usernames, private URLs, generated review outputs, and Wiki worktrees remain uncommitted.

## Stage 3P - Deterministic image transform suite

Stage 3P adds deterministic local page-image transforms, contact sheets, split/mirror previews, component overlays, review metrics, and a local visual review index. Generated artefacts remain ignored. It does not use OCR, AI/ML, image-derived cipher execution, OutGuess, Discord processing, CUDA, canonical corpus activation, page-boundary finalization, or solve claims.

## Stage 3Q - Redacted Discord AI-review bundles

Stage 3Q adds redacted Discord AI-review bundles and topic shards from local admin-provided exports and Stage 3N/3O generated records. Generated shards remain ignored, the committed aggregate contains counts only, and no raw logs, usernames, private URLs, AI upload, live Discord, scraping, CUDA, or solve claim is introduced.

## Stage 3R - Discord lead promotion audit

Stage 3R audits redacted Stage 3Q leads, promotes selected public-source and exact-observation records, preserves known false-positive classes as negative controls, and creates the first disabled post-Discord manifests. It does not execute experiments, publish raw Discord content, use CUDA, activate canonical corpus, finalize page boundaries, or claim a solve.

## Stage 3S - Onion 7 explicit seed-pack execution

Stage 3S executes only `EXP-3R-003`, the bounded Onion 7 explicit seed pack. It uses the reviewed raw 4x4 table and reviewed derived value spaces, enumerates the declared routes, directions, and reset modes, applies Stage 3C calibrated scoring, and writes candidate outputs only under ignored paths. The result is inconclusive and no solve claim is made.

## Stage 3T - GP/rune claim verifier

Stage 3T executes only `EXP-3R-004`, the bounded GP/rune claim verifier. It recomputes exact GP-sum, rune-count, residue, prime-status, and derived numeric claims where exact spans or explicit values exist, classifies unsupported claims without broadening into span search, and writes generated verification outputs only under ignored paths. No raw Discord logs or page images are processed and no solve claim is made.

## Stage 3U - Cookie signed variant pack

Stage 3U executes only `EXP-3R-001`, the bounded cookie SHA-256 signed-variant pack. It expands only manifest-declared signed/public strings and byte variants, uses UTF-8 and SHA-256 only, writes generated hash outputs under ignored paths, and finds zero exact matches. No fuzzy matching, partial matching, hashcat, CUDA, live Tor, raw Discord processing, page-image processing, or solve claim is made.

## Stage 3V - OutGuess regression harness

Stage 3V implements the bounded OutGuess regression harness. The local run had no OutGuess binary, so enabled cases were skipped as missing-tool records. Raw historical artefacts and extracted payloads remain ignored, and no broad stego scan or solve claim is made.

## Stage 3W - State consolidation and anti-drift hardening

Stage 3W consolidates persistent project context after Stage 3V. It repairs stale current-state wording, defines the source-of-truth hierarchy, adds anti-drift checks, updates CI scripts and tests, and does not execute experiments, process raw data, use CUDA, activate the canonical corpus, finalize page boundaries, or claim a solve.

## Stage 3X - CLI modularisation without behavior change

Stage 3X split the growing `libreprimus.cli` module into focused command modules while preserving command names, options, output shape, tests, and behavior. This is a maintenance stage only, not an experiment stage.

## Stage 3Y - Result synthesis and retirement ledger

Stage 3Y summarizes noisy, negative, inconclusive, verified, and deferred Stage 3 results into `docs/roadmap/staged-plan.md` and `data/research/` ledgers so future work does not repeat already-bounded tests without a new manifest and rationale. It adds `libreprimus research-synthesis` validation, anti-drift coverage, and documentation freshness policy. No experiments are executed and no solve claim is made.

## Stage 3Z - Source-of-truth and newcomer map

Stage 3Z expands the source-of-truth hierarchy into concise onboarding maps that point humans, Codex sessions, Deep Research, contributors, and reviewers to the right operational docs, staged plan, research logs, schemas, modules, and generated-output policies.

## Stage 4A - Full Discord research-bundle extraction for Deep Research

Stage 4A converted local admin-provided Discord HTML exports into redacted, scoped, image-aware Deep-Research-friendly bundles. Raw Discord logs, private attachments, usernames, user IDs, message IDs, and private URLs remain local/ignored and must not be committed.

The independent review originally suggested CPU batch transform API extraction as Stage 4A. User direction after Discord website review moved full Discord research-bundle extraction earlier. Stage 4H later completed CPU batch API extraction, Stage 4I completed scorer consolidation, Stage 4Q recorded benchmark/parity planning, Stage 5A recorded CUDA planning, and Stage 5B completed the harness skeleton before any CUDA implementation work.

## Stage 4B - Website-derived source-lock triage and visual observation intake

Stage 4B triages website/public-source findings and visual observations into source-lock, observation, and negative-control records without raw image publication or solve claims. It promotes allowlisted public sources only, rejects unsafe/private or noisy links, preserves ambiguity, and keeps all queued manifests disabled.

## Stage 4C - Cuneiform and dot annotation pack

Create a bounded review workflow for cuneiform, dot, and motif annotations. Record exact coordinates, ambiguity tables, alternate readings, review status, and negative controls before any cuneiform/dot item can become an experiment seed.

## Stage 4E - cicada-solvers/iddqd source-lock delta audit

Stage 4E is complete. It records metadata for selected `cicada-solvers/iddqd` paths and future image/stego/audio provenance work. It does not mirror the repository or commit raw artefacts.

## Stage 4F - OutGuess/audio historical fixture source-locking

Stage 4F is complete. It source-locks historical OutGuess/audio fixture metadata for selected public paths and promoted pages, records toolchain requirements for OutGuess, OpenPuff, MP3Stego, hexdump/strings, and audio rendering, and queues disabled future manifests without downloading or committing raw artefacts.

## Stage 4N - OutGuess/audio positive-control completion

Stage 4N is complete. It records OutGuess/audio readiness, fixture-cache status, expected-output
requirements, toolchain availability, and synthetic controls. Historical cases remain blocked
until assets, expected outputs, and tools are ready. No OutGuess, OpenPuff, MP3Stego, spectrogram,
hexdump/string scan, or extraction was executed.

## Stage 4O - CPU batch adapter expansion

Stage 4O is complete. It expands CPU batch adapter coverage with solved-fixture-safe streams,
deterministic parity expectations, adapter coverage records, and score-summary compatibility checks.
It records `9` supported adapters, `2` missing/deferred adapters, and `8` parity expectations
without adding CUDA or changing transform semantics.

## Stage 4P - result-store and score-summary unification

Stage 4P is complete. It unifies committed summaries and optional ignored generated outputs into
source inventory records, unified result records, Stage 4I-compatible score summaries,
method-status joins, and a compact cross-stage report. It records `18` source inventory records,
`82` unified result records, `82` unified score-summary records, and `82` method-status joins.
Generated JSON/JSONL/SQLite result bodies remain ignored and no new scorer, experiment execution,
CUDA work, canonical corpus activation, page-boundary finalization, or solve claim was added.

## Stage 4Q - CPU benchmark and parity planning

Stage 4Q is complete. It records `5` benchmark plan records, `14` parity readiness records,
`3` CPU smoke diagnostic records, `9` future CUDA targets ready for planning, `2` blocked
targets, and `3` skipped non-CUDA targets. Generated records remain ignored under
`experiments/results/benchmarks/stage4q/`, and `codex-output/` handoff files remain ignored.
Stage 4Q did not implement CUDA, run GPU benchmarks, claim speedups, run broad experiments,
activate the canonical corpus, finalise page boundaries, or make solve claims.

## Stage 5A - CUDA planning and parity scaffolding

Stage 5A is complete. It records `14` CUDA target-plan records, `9` ready planning targets,
`2` blocked targets, `8` explicit non-target records, `9` parity scaffold records, and `10`
satisfied implementation gates. Generated reports remain ignored under
`experiments/results/cuda-planning/stage5a/`, and `codex-output/` handoff files remain ignored.
Stage 5A did not add or modify CUDA source, run GPU benchmarks, claim speedups, run broad
experiments, process raw data, activate the canonical corpus, finalise page boundaries, or make
solve claims.

## Stage 5B - CUDA parity harness skeleton

Stage 5B is complete. It records `14` CUDA parity harness plans, `14` parity fixture records,
`3` backend capability records, and `9` future-kernel matrix rows. The local 16GB GPU profile is
recorded only as optional planning metadata; compatibility 8GB and CI no-GPU profiles remain
first-class.

Generated reports remain ignored under `experiments/results/cuda-parity/stage5b/`, and
`codex-output/` handoff files remain ignored. Stage 5B did not add or modify CUDA source, add GPU
kernels, run GPU benchmarks, claim speedups, run broad experiments, process raw data, activate the
canonical corpus, finalise page boundaries, or make solve claims.

## Stage 5C - CUDA build and device-detection scaffold

Stage 5C is complete. It records `3` CUDA build-profile records, `3` toolchain detection records,
`3` device detection records, and `1` optional smoke-build record. The local 16GB GPU profile is
recorded only as optional metadata; compatibility 8GB and CI no-GPU profiles remain first-class.

Generated reports remain ignored under `experiments/results/cuda-build/stage5c/`, and
`codex-output/` handoff files remain ignored. Stage 5C did not add or modify CUDA source, add GPU
kernels, run CUDA tests, run GPU benchmarks, claim speedups, run broad experiments, process raw
data, expand the website, activate the canonical corpus, finalise page boundaries, or make solve
claims.

## Stage 5D - native C++ CPU batch backend and deterministic threading baseline

Stage 5D is complete. It records `1` native backend capability record, `5` threading records, `1`
native/Python parity record, and `1` diagnostic record. Thread counts `1`, `2`, `4`, `8`, and `16`
produce the same output hash for the synthetic fixture:
`76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66`.

Generated reports remain ignored under `experiments/results/native-cpu/stage5d/`, and
`codex-output/` handoff files remain ignored. Stage 5D did not add or modify CUDA source, add GPU
kernels, run CUDA transforms, run GPU benchmarks, claim speedups, run broad experiments, process raw
data, expand the website, activate the canonical corpus, finalise page boundaries, or make solve
claims.

## Stage 5E - first CUDA kernel contract and CPU/native parity adapter selection

Stage 5E is complete. It selects `shift_score_kernel` as the first future CUDA kernel contract,
with target `stage5a-caesar_mod29-cuda-target`, transform family `caesar_mod29`, and adapter
family `native_cpu_synthetic_shift_adapter`. It records `3` alternate candidates and `10`
blocked/rejected candidates.

The selected contract cites the Stage 5D one-thread and multi-thread native output hash
`76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66` and keeps Python/native
parity `true`. Generated reports remain ignored under
`experiments/results/cuda-kernel-contract/stage5e/`, and `codex-output/` handoff files remain
ignored. Stage 5E did not add or modify CUDA source, add GPU kernels, run CUDA transforms, run GPU
benchmarks, claim speedups, run broad experiments, process raw data, expand the website, activate
the canonical corpus, finalise page boundaries, or make solve claims.

## Stage 5F - first synthetic-only CUDA parity kernel implementation

Stage 5F is complete. It adds only the selected `shift_score_kernel` CUDA target for the Stage 5D
synthetic uppercase Latin shift fixture, keeps the fixture text and shifts fixed, and records the
native/CUDA synthetic parity hash
`76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66`.

Generated reports remain ignored under `experiments/results/cuda-kernel/stage5f/`, and
`codex-output/` handoff files remain ignored. Stage 5F does not run real Liber Primus data through
CUDA, run solved or unsolved page CUDA transforms, run GPU benchmarks, claim speedups, run broad
experiments, process raw data, expand the website, activate the canonical corpus, finalise page
boundaries, or make solve claims.

## Stage 5G - shift_score CUDA parity reporting and solved-fixture-safe adapter preflight

Stage 5G is complete. It records one shift_score parity report, one CUDA device-code subset audit,
one solved-fixture-safe adapter preflight record, and one aggregate summary under `data/cuda/`.
The Stage 5F native/CUDA synthetic hash remains
`76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66`.

Stage 5G refactors CUDA-facing `.cu` and `.cuh` code away from STL, exceptions, dynamic allocation,
and host convenience types at the kernel boundary. Generated reports remain ignored under
`experiments/results/cuda-parity-reporting/stage5g/`, and `codex-output/` handoff files remain
ignored. Stage 5G does not add new CUDA kernels, run real Liber Primus data, run solved or unsolved
page CUDA transforms, run GPU benchmarks, claim speedups, process raw data, expand the website,
activate the canonical corpus, finalise page boundaries, or make solve claims.

## Stage 5H - Gematria mod-29 shift_score contract and native parity fixture preparation

Stage 5H is complete. It records one Gematria mod-29 shift-score contract, one synthetic numeric
native parity fixture, five blocked solved-fixture-safe mapping records, one score-summary parity
plan, and one aggregate summary under `data/cuda/`. The Gematria fixture uses numeric tokens
`0..28`, arithmetic direction `forward_add_shift_mod29`, and separator preservation. Its expected
output hash is `a6d5d5161145fd31ab429a8e955e0412d7b0af6089f06ee8b33baf8cd00b27a0`, which is not
the Stage 5F uppercase Latin synthetic hash.

Generated reports remain ignored under `experiments/results/gematria-shift-contract/stage5h/`, and
`codex-output/` handoff files remain ignored. Stage 5H does not add CUDA kernels, run CUDA
transforms, run real Liber Primus data, run solved or unsolved page CUDA transforms, run GPU
benchmarks, claim speedups, process raw data, expand the website, activate the canonical corpus,
finalise page boundaries, or make solve claims.

## Stage 5I - Gematria mod-29 shift_score synthetic CUDA parity preparation

Stage 5I is complete. It records one kernel-preparation record, one CUDA-C ABI plan record, one
validation-vector record, one implementation-checklist record, and one aggregate summary under
`data/cuda/`. The future target remains `gematria_mod29_shift_score_kernel` over numeric tokens
`0..28`, transformable masks, candidate-major output ordering, and preserved separator placeholders.

Generated reports remain ignored under `experiments/results/gematria-cuda-prep/stage5i/`, and
`codex-output/` handoff files remain ignored. Stage 5I does not add CUDA source, add kernels, run
CUDA transforms, run real Liber Primus data, run solved or unsolved page CUDA transforms, run GPU
benchmarks, claim speedups, process raw data, expand the website, activate the canonical corpus,
finalise page boundaries, or make solve claims.

## Stage 5J - Gematria mod-29 shift_score synthetic CUDA parity kernel implementation

Stage 5J is complete. It records one implementation record, one build record, one synthetic parity
record, and one aggregate summary under `data/cuda/`, and adds exactly one CUDA kernel:
`gematria_mod29_shift_score_kernel`.

The kernel applies `(token + shift) % 29` to transformable numeric tokens `0..28`, preserves
non-transformable separator placeholders by mask, writes deterministic candidate-major output, and
matches the Stage 5H native fixture hash
`a6d5d5161145fd31ab429a8e955e0412d7b0af6089f06ee8b33baf8cd00b27a0`. The Stage 5F uppercase
Latin synthetic hash remains separate. Generated reports remain ignored under
`experiments/results/gematria-cuda-kernel/stage5j/`, and `codex-output/` handoff files remain
ignored. Stage 5J does not run real Liber Primus data, run solved or unsolved page CUDA transforms,
run GPU benchmarks, claim speedups, process raw data, expand the website, activate the canonical
corpus, finalise page boundaries, or make solve claims. Stage 5K Gematria shift_score CUDA parity
reporting and solved-fixture-safe preflight is next.

## Stage 4G - Cookie exact-candidate refresh

Stage 4G is complete. It refreshed only explicit source-backed cookie candidate strings, tested `4`
deduplicated candidates against `2` historical targets for `8` SHA-256 exact comparisons, found `0`
exact matches, and kept generated records ignored under `experiments/results/cookie-refresh/stage4g/`.
Do not rerun cookie work without newly source-locked exact candidate strings.

## Stage 4H - CPU batch transform API extraction

Stage 4H is complete. It added `libreprimus cpu-batch`, CPU batch schemas, synthetic and solved-baseline-safe manifests, deterministic result hashes, adapter coverage, scoring adapter integration, and a CUDA parity contract. The local smoke batch executed `6` CPU-only candidates and supported all `6` current registry transforms.

## Stage 4I - Scorer consolidation and calibration report

Stage 4I is complete. It consolidated scorer definitions and calibration reports before CPU batch APIs are used for broader campaigns or future transform-and-score CUDA parity.

## Phase 1 - Corpus and known-solution reproduction

Load locked corpus data and reproduce known solved-page behavior before new search work.

## Phase 2 - CPU cryptanalysis workbench

Implement CPU reference transforms, scorers, manifest runner, result sink, and null controls.

## Phase 3 - GPU prototype

Add CUDA kernels only for tested CPU reference transforms and prove parity.

## Phase 4 - Full experiment engine

Support branching search, structured result review, resumable runs, and manifest determinism.

## Phase 5 - Serious search campaigns

Run bounded, reviewed campaigns with pinned data and clear stop conditions.

## Phase 6 - Advanced methods

Evaluate statistical, language-model-assisted, or search-prior methods only after baseline controls exist.

## Phase 7 - Publication and reproducibility

Prepare reproducible reports, source citations, data locks, and review notes.

<!-- BEGIN stage5ef -->
## Stage 5EF Route

Stage 5EF is complete as current-truth and drift-audit infrastructure. It preserves Stage 5EE and routes the
deferred number-fact review batch 006 to Stage 5EG.

Next: Stage 5EG - Source-lock number-fact review batch 006, without execution.
<!-- END stage5ef -->

<!-- BEGIN stage5eg -->
## Stage 5EG Routing

- Complete: Stage 5EG - Post-edit doc-staleness guardians, read-only auditor agents, stop-hook drift gate, and daily automation setup, without puzzle execution.
- Next: Stage 5EH - Lag5 phenomenon source-lock, diagnostic/probe manifest, and enriched fact cards, without execution.
- Then: Stage 5EI - Source-lock number-fact review batch 006, without execution.
<!-- END stage5eg -->

<!-- BEGIN stage5eh -->
## Stage 5EH Routing

- Complete: Stage 5EH - Lag5/outguess/byte-string/red-number/F5 context source-lock addendum, diagnostic probe manifests, and enriched fact cards, without execution.
- Next: Stage 5EI - Source-lock number-fact review batch 006, without execution.
- Batch 006 remains deferred to Stage 5EI.
<!-- END stage5eh -->
<!-- BEGIN stage5ei current-state -->

<!-- stage6:start -->
## Stage 6 Roadmap Update

Stage 6 completed the diagnostic backlog readiness foundation without execution. Stage 6B should finalize the finite Stage 7 probe manifest and archive-run contract. Stage 7 remains the earliest bounded diagnostic execution stage after Stage 6B, Stage 8 remains triangle readiness, and Stage 9 remains earliest bounded triangle experiments.
<!-- stage6:end -->

<!-- stage6b:start -->
## Stage 6B Route

Stage 6B completed triage repair and hook stabilization without execution. Next: Stage 6C - Final finite Stage 7 probe manifest and archive-run contract, without execution. Stage 7 execution, ZIP archive creation, Stage 8 triangle readiness, and Stage 9 experiments remain blocked.
<!-- stage6b:end -->

<!-- stage6c:start -->
## Historical Stage 6C Roadmap Note

At the time of Stage 6C, Stage 6C - OUROBOROS / I=31 circumference / Page32 spiral geometry source-lock addendum, without execution was the latest completed stage.

Historical next route at Stage 6C closeout: Stage 6D - Final finite Stage 7 probe manifest and archive-run contract, without execution. Stage 6D must consume the Stage 6C source-locked facts and future-probe addendum before finalizing any finite Stage 7 manifest. Stage 7 execution is still blocked.
<!-- stage6c:end -->

<!-- stage6d:start -->
## Stage 6D Roadmap Note

Current completed stage: Stage 6E - Readiness consolidation, bridge source-locks, hook/doc-staleness repair, and Stage 6F manifest inputs, without execution.

Next: Stage 6F - Final finite Stage 7 probe manifest and archive-run contract, without execution. Stage 6E must consume both the Stage 6C OUROBOROS/I31 addendum and the Stage 6D doublet/boundary-policy addendum before any finite Stage 7 manifest can be finalized.
<!-- stage6d:end -->

<!-- stage6e:start -->
## Stage 6E Current Boundary

Current completed stage: Stage 6E - Readiness consolidation, bridge source-locks, hook/doc-staleness repair, and Stage 6F manifest inputs, without execution.

Current work: Stage 6F - Final finite Stage 7 probe manifest and archive-run contract, without execution.

Stage 6E classified all stale-current warning-domain findings into named buckets, installed bounded report-only preprompt doc-staleness advisory behavior, source-locked finite bridge facts, superseded the stale Stage 6B Stage 6C token-block projection precondition, and built Stage 6F source-root/probe traceability inputs.

Stage 6E did not create a final Stage 7 manifest, finalize an archive-run contract, create a result archive, run probes, generate route or byte streams, run OCR/image/stego/CUDA/scoring/benchmarks, select targets, or make a solve claim.
<!-- stage6e:end -->
