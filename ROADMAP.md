# Roadmap

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

## Stage 3L - Deterministic image/audio/web analysis CLIs

After Stage 3K succeeds, add deterministic image/audio/web analysis CLIs or a bounded cookie-hash preimage pack. Any image-derived numeric seed must first pass observation review and policy checks. Do not jump to CUDA.

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
