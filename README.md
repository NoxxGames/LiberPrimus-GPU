# liberprimus-gpu

[![CI](https://github.com/NoxxGames/LiberPrimus-GPU/actions/workflows/ci.yml/badge.svg)](https://github.com/NoxxGames/LiberPrimus-GPU/actions/workflows/ci.yml)

## Mission

`liberprimus-gpu` is a reproducible research workbench for conservative Liber Primus cryptanalysis experiments. The project keeps corpus provenance, solved baselines, transform metadata, run records, and CI gates ahead of any exploratory search or GPU acceleration work.

## Current boundaries and deferred work

These are not permanent project exclusions unless marked as safety rules. They describe the current implementation boundary after Stage 5CW operator-decision readiness integration and real-decision package preflight. Future experiments must stay bounded, reviewable, and reproducible before larger campaigns begin. CUDA and broad campaigns are deferred, not permanently excluded.

### Permanent safety rules

- No generated output is a solve by itself.
- No Liber Primus page is claimed solved; material that is still unsolved must not receive a solve claim without a pinned corpus, manifest, transform chain, reproducible output, tests, and review.
- Raw data must not be overwritten or committed.
- Generated outputs and SQLite databases must not be committed.

### Current boundaries

- Canonical corpus: inactive.
- Page boundaries: reviewable.
- Broad unsolved-page search campaigns: not started.
- Scoring campaigns: not started; Stage 3A/3B minimal triage scoring exists only for sorting and inspecting bounded 841-candidate CPU runs, Stage 3C calibration uses small local controls only, Stage 3D applies that scorer to a four-key explicit Vigenere preview only, Stage 3F applies it to the bounded 48-candidate LP evidence-key Vigenere pack only, Stage 3G applies it to a bounded 256-candidate p56-local prime-minus-one offset sweep only, Stage 3H applies it to a bounded 64-candidate reset/advance ablation with 100 negative controls only, Stage 3I applies it to a bounded 56-candidate historical motif Vigenere pack only, Stage 3J applies it to a bounded 192-candidate Mersenne/perfect-number stream probe only, and Stage 3S applies it to the bounded 72-candidate Onion 7 explicit seed pack only. Stage 4I consolidates these score labels and calibration records as triage-only metadata, not solve evidence.
- Visual/image-derived observations: registry and deterministic feature summaries only, plus deterministic review transforms; Stage 3K records source locks and reviewable observations, Stage 3M records deterministic local image features, and Stage 3P generates ignored review transforms/contact sheets. No image-derived text experiments are executed.
- Cookie/hash preimage work: Stage 3L tests two explicit SHA-256 packs only, Stage 3U tests the manifest-declared signed/public string variant pack only, and Stage 4G refreshes source-backed Stage 4B strings only. All use exact byte-string logging with no fuzzy, partial, dictionary, hashcat, GPU, or solve claims.
- Stego/OutGuess work: Stage 3V adds a deterministic OutGuess regression harness only. Stage 4F adds fixture source-lock metadata and toolchain requirements only. Missing tools/assets are explicit skipped outcomes, generated payloads stay ignored, and no broad image scan, stego extraction, audio scan, or payload interpretation is performed.
- Discord source discovery: Stage 3N scans admin-provided local HTML exports only and commits aggregate/redacted records only. Stage 3O promotes a bounded, public-safe subset of redacted source-discovery records. Stage 3Q builds ignored redacted topic shards for local AI/deep-research review. Stage 3R audits those leads, promotes only corroborated public/source-observation records, preserves false positives as negative controls, and queues disabled post-Discord manifests. Raw logs, message bodies, usernames, and private attachment URLs are not committed.
- Full Discord review bundles: Stage 4A builds redacted chronological streams, channel shards, topic shards, indexes, an LP page gallery, and an SFTP-ready static site under ignored paths for Deep Research handoff. Raw Discord logs, usernames, user IDs, message IDs, private URLs, generated static site files, copied LP page images, thumbnails, archives, and generated bundle outputs are not committed.
- Source-lock and visual observation intake: Stage 4B promotes allowlisted public-source records only, records source-health metadata, preserves cuneiform/delimiter/dot/number-square/cookie observations as review-only and non-canonical, and stores false-positive classes as negative controls. No Stage 4B visual observation is an experiment seed.
- Visual annotation: Stage 4C creates cuneiform, delimiter, dot-pattern, number-square-reference, and visual negative-control annotation tasks plus a generated local annotation site and blank coordinate templates. Coordinates and readings are separate; no Stage 4C visual task is verified, canonical, or usable as an experiment seed.
- Bounded numeric verification: Stage 4D runs only no-fudge numeric and metadata audits. GP/rune batch002 skips without exact new spans, number-square routes skip without locked raw values, delimiter/dot audits infer no meaning, cuneiform seed execution remains deferred, and cookie pack v2 is deferred to a future explicit stage.
- Source-delta audits: Stage 4E records selected `cicada-solvers/iddqd` tree metadata only. It does not blind-mirror external repositories, commit raw images/audio/fonts/binaries, run stego tools, or infer meaning from compression artefacts.
- Public source-lock snapshots: Stage 4K locks a small allowlisted public-source subset with metadata, canonical URLs, retrieval status, hashes where fetched, copyright notes, explicit snapshot policies, and GitHub commit-addressed references. It does not broad crawl, blind-mirror repositories, commit full HTML by default, or commit binary/image/audio/font/archive artefacts.
- Cicada source harvester: Stage 5AF adds local-only source-manifest, dry-run planning, hash/inventory/extraction, and research-bundle scaffold tooling. Stage 5AG runs that tooling against user-provided ignored `third_party/` material and commits compact local source inventory, manifest linkage, source-lock candidate, gap, research-bundle readiness, and guardrail metadata only. Stage 5AH repairs operational doc staleness coverage before extraction continues. Stage 5AI creates ignored curated research-input bundle scaffolds plus compact source-card, content-index, website-ingest, Deep-Research pack, missing-source, and guardrail metadata. Stage 5AJ integrates ignored `third_party/UsefulFilesAndIdeas/` local workbooks/text/image metadata, important-link indexes, source-card/content-index updates, extraction-fidelity policy, redaction policy, and scraper-capture profiles while keeping private Deep Research extracts minimally redacted and public website views conservative/review-gated. Stage 5AK integrates ignored `third_party/UsefulFilesAndIdeas/community-facts/` message and attachment metadata, claim records, correction logs, and arithmetic preflight checks as review-only community observations. Stage 5AL creates the committed metadata-only website-ingest package and private Deep Research export contract while keeping public website-ready at `0`. Stage 5AM renders that metadata into an ignored uploadable private static index at `website-export/stage5am/research-index/` with no raw bodies or private identifiers. Stage 5AN builds an ignored private content pack, hosted private-content export, and combined SFTP-ready webroot under `deep-research-content-packs/stage5an/` and `website-export/stage5an/` for private Deep Research handoff. Network fetching/cloning remains deferred, Google Drive must not be used as project storage, local archive/workbook/community listings and generated extracts are not source truth, and raw source files remain ignored and uncommitted.
- Page 49-51 token block: Stage 5AP creates metadata-only source locks, canonical 32x8 token transcription, logical coordinate records, primary-60 alphabet/mapping preflight, null-control planning, Deep Web Hash context, and OutGuess positive-control guardrails. Stage 5AR adds original-image source locks, source-backed 10/13/9 page-split records, 256 original-image pixel-coordinate records, coordinate validation, and case-ambiguity policy. Stage 5AT packages the 9 active token-case ambiguity classes into 203 human-review challenges plus 212 canonical-transcription challenge records. Stage 5AU records that first pack as count-valid but not usable for decisions, then rebuilds a v2 ignored review pack with glyph-candidate crops, context crops, row context, overlays, full challenge visibility, and blank decision templates while keeping the canonical transcription unchanged. Stage 5AV integrates the filled local decision template as metadata only, confirming 126 current tokens, preserving 77 unresolved variant branches, and creating compact branch-manifest records without changing canonical transcription or generating variant byte streams. Stage 5AW repairs a Stage 5AV parser-quality issue by excluding prose fragments from reviewer-extra possible tokens, preserving visual placeholders separately, and rebuilding superseding branch metadata. Stage 5AX inserts opt-in parallel validation infrastructure. Stage 5AY consumes the repaired Stage 5AW branch metadata to design bounded future preflight manifests, branch eligibility, controls, branch budgets, result schema previews, DWH context, and execution gates without generating byte streams or executing experiments. Stage 5AZ repairs the duplicated `unresolved_as_current_only` family ID by keeping one family record with both baseline and unresolved-policy taxonomy memberships and supersedes the Stage 5AY bounded variant-family manifest for review. Stage 5BB canonicalises active-manifest precedence, validates the Stage 5AY branch-eligibility policy, blocks stale Stage 5AV/5AY active loads, and creates a no-execution runner scaffold. Stage 5BD implements deterministic dry-run plan IDs, future result-path validation, family counters, fixture-only records, archive marker policy, and validation-evidence consolidation while preserving the no-byte-stream boundary. Stage 5BF pauses deeper token-block planning to source-lock the 2012-2017 historical route corpus and technique taxonomy for Deep Research review. Stage 5BI records Fandom / Uncovering Cicada context, 2014 surfaces, spreadsheet metadata, archive crosswalk candidates, negative controls, and source gaps without changing page 49-51 active records. Stage 5BJ closes the exact 2014 surface archive crosswalks and boards/media equivalence metadata while keeping Fandom page bodies and token-block execution blocked. Stage 5BK integrates those historical-route constraints, source-locks iddqd-v2 as compact metadata, records String 4 page49-51 matrix-hex context, and keeps active token-block records unchanged. Stage 5BM integrates Stage 5BL findings and classifies String 4 as a partial branch match against Stage 5AW metadata: 249 canonical matches, 6 Stage 5AW-supported noncanonical positions, and 1 unsupported position. Stage 5BN audits that single unsupported position, records target-only local spreadsheet support for `0l`, proposes an inactive review-only addendum, and keeps active records plus all execution gates blocked. Stage 5BO source-locks the original and corrected ignored decision templates, records 8 compact operator errata, builds an inactive errata-aware planning universe, and reclassifies String 4 as a full branch match for planning only: 249 canonical matches, 6 Stage 5AW-supported noncanonical positions, 1 operator-errata-supported noncanonical position, and 0 unsupported positions. Stage 5BQ consumes the Stage 5BP review outcome, records that full-branch status as inactive planning context only, blocks String 4 active input and dry-run ingestion now, adds fail-closed future dry-run requirements, and preserves Stage 5BD dry-run records. Stage 5BS then integrates the Stage 5BR accept-with-warnings review outcome by adding a closed planning-ingestion gate, fail-closed future-runner citation policy, inactive-sidecar consumption policy, active-ingestion blocker, reviewable source-digest/validation evidence, and Stage 5BT review routing. Stage 5BU repairs the Stage 5BS preserved active-lineage path for the Stage 5AW repaired branch manifest, adds erratum/digest/validation records, and hardens Stage 5BS validation while keeping the gate closed. Stage 5BW consumes Stage 5BV findings, proposes a future inactive-sidecar planning-ingestion model, creates manifest-supersession preflight records without superseding active manifests, preserves Stage 5BD run-plan IDs, and routes the closed proposal to Stage 5BX review. Stage 5BY consumes the Stage 5BX review outcome, classifies the Stage 5BW source-digest duplicates, adds record-family filename-equivalence metadata, creates an inactive planning manifest scaffold and no-execution planning-ingestion sidecar, preserves Stage 5BD run-plan IDs, and routes the metadata to Stage 5BZ review. Stage 5CI consumes the Stage 5CH review outcome, hardens future operator approval, Deep Research acceptance, combined approval-gate, and activation-decision templates, and keeps every approval, activation, no-byte, no-execution, supersession, and String 4 gate unsatisfied or closed. Stage 5CK consumes the Stage 5CJ review outcome, creates fixture-only approval/acceptance/activation-decision validation packs and a review package, proves fixture records cannot satisfy real gates, preserves Stage 5CI/5CG/5CE/5CC/5BD records, and selects Stage 5CL review. Stage 5CM consumes the Stage 5CL review outcome, preserves Stage 5CK fixture-only packs, hardens fixture-vs-real approval boundaries, adds end-to-end readiness-boundary validation and credential-redaction policy, caps Stage 5CM-and-later local parallel validation at 8 workers, and selects Stage 5CN review. Stage 5CO consumes the Stage 5CN review outcome, packages the future real approval/acceptance/combined-gate/activation transition path as metadata, records current missing requirements, keeps real records absent, and selects Stage 5CP review. Stage 5CQ consumes the Stage 5CP review outcome, preserves the Stage 5CO readiness and transition records, creates only a future operator-decision package scaffold, restores strict `codex-output` handoff discipline, keeps real decisions absent, and selects Stage 5CR review. The block remains inactive, not decoded, not treated as intentional evidence, not used for hash/preimage search, and not an experiment seed.
- Parallel validation: Stage 5AX adds an opt-in local `libreprimus parallel-validation` harness and `scripts/ci/run-parallel-validation.*` wrappers that run explicitly read-only validation commands concurrently and use pytest-xdist when available or deterministic subprocess sharding otherwise. Git, GitHub, network/remote, generated-output-writing, commit/push, issue-update, and cryptanalytic commands remain serial or blocked. The existing CI path remains conservative unless a future prompt explicitly opts into the harness.
- Observation promotion ledger: Stage 4L joins Stage 4J review decisions with Stage 4K source locks and records ready, blocked, deferred, quarantined, rejected, source-reference-only, and control-only states. Ready does not mean executed; all future manifests remain disabled.
- Image source-variant and compression preflight: Stage 4M scans ignored local LP page images for metadata and deterministic metric-only compression summaries, records source-variant comparison readiness, keeps star-like/compression-like artefacts review-only, and keeps the bigram/Fibonacci-421 observation blocked pending reproducible matrix and null controls. It does not commit raw images, generated visualisations, or execute image/bigram experiments.
- Stego/audio positive-control readiness: Stage 4N records fixture readiness, cache policy, expected-output requirements, toolchain state, and synthetic controls. Historical OutGuess/OpenPuff/MP3/audio cases remain blocked until assets, exact expected outputs, and tools are ready.
- CPU batch transform API: Stage 4H provides deterministic CPU-only input stream, transform candidate, result, summary, adapter coverage, and parity-contract records. Later stages extend this into result-store, benchmark-planning, CUDA-contract, native-conformance, prime-minus-one, synthetic CUDA parity, Stage 5AC compact reporting/bounded-p56 preflight metadata, the Stage 5AD bounded p56 CUDA mismatch record, the Stage 5AD-fix reference-contract investigation, and Stage 5AE corrected formula-parity reporting. Stage 5AB adds a document staleness gate over those operational claims; Stage 5AH hardens it with stage-ledger truncation, operational-file-map coverage, and current/next-stage checks so README-like ledgers cannot silently stop at older stages. This is infrastructure for future native/CUDA parity, not a broad experiment runner.
- Scoring contract: Stage 4I provides scorer inventory, finite confidence-label records, compatibility mappings, calibration-profile/report records, and CPU batch score compatibility checks. Score labels can create review leads only and cannot imply solved plaintext.
- Post-Discord experiment execution: Stage 3S executes only `EXP-3R-003`, the bounded Onion 7 explicit seed pack. Stage 3T executes only `EXP-3R-004`, the GP/rune claim verifier. Stage 3U executes only `EXP-3R-001`, the cookie SHA-256 signed-variant pack. All keep generated records under ignored paths and make no solve claim.
- CUDA experiment campaigns: not started.
- Normal bounded local CPU experiments: allowed automatically when they pass `experiments/policies/operator-policy-v0.yaml`.
- Broad unsolved-page campaigns: not started.
- Approval packets: optional/high-risk audit tooling, not the default path for policy-passing bounded CPU items.
- Existing CUDA code and metadata are summarized by the latest staged-plan and CUDA notes; broad CUDA and unsolved-page CUDA remain blocked unless an explicit future prompt scopes them with matching CPU references, parity tests, and benchmark plans.

### Deferred future work

- Stage 5CX - Deep Research review of Stage 5CW operator-decision readiness integration and real-decision package preflight, without execution.
- Website expansion is deferred to a future unnumbered project.
- Future visual numeric observations for base-60 or cuneiform-like numbers, binary dot patterns, symmetry/asymmetry, and page imagery must remain reviewable before becoming experiment seeds.
- Search campaigns.
- CUDA kernels after CPU references and parity tests exist.
- Benchmark campaigns after stable CPU/GPU baselines exist.

### Already implemented since Stage 0A

- Profile and corpus-candidate infrastructure.
- Ten known solved baseline fixtures.
- CPU transform registry.
- Solved-baseline manifest runner.
- JSONL/SQLite result-store foundation.
- Raw-data-free GitHub Actions CI.
- CI-gated consistency checks.
- CPU exploratory experiment dry-run planner.
- Bounded CPU execution harness for synthetic and solved-fixture-only runs.
- Exploratory experiment proposal and human-approval workflow.
- Approval-gated execution path for approved synthetic/solved controls.
- First real bounded exploratory approval-readiness packet.
- Standing bounded local CPU operator policy and queue scaffold.
- Minimal CPU Caesar plus affine executor and triage scoring for the first `841` candidate bounded queue item.
- Candidate lead inspection, refined triage scoring, reranking, and reverse-direction bounded comparison.
- Scoring calibration with positive controls, null controls, negative controls, tiny crib checks, and a conservative Stage 3D queue recommendation.
- Small explicit-key Vigenere preview for the four declared known-motif keys, with calibrated scoring and ignored generated outputs.
- Deep Research method backlog ingestion, deterministic Stage 3E queue counts, and dry-run executor-support classification.
- Reset/advance-aware Stage 3F LP evidence-key Vigenere pack executor and 48-candidate run.
- Bounded Stage 3G p56-local prime-minus-one offset sweep executor and 256-candidate run, plus a queued future Mersenne/perfect-number probe.
- Shared Stage 3H reset/advance state machine, 64-candidate ablation run, and 100 family-specific negative controls.
- Bounded Stage 3I historical motif Vigenere pack run for 14 declared keys and 56 candidates.
- Bounded Stage 3J Mersenne/perfect-number stream probe for the finite declared exponent sequence and 192 candidates.
- Stage 3K historical archive/source-lock, local image metadata, visual numeric observation, and cookie/hash artefact registry.
- Stage 3L bounded SHA-256 cookie-hash preimage packs for the two archived 2013 cookie artefacts.
- Stage 3M deterministic local image-analysis CLI and visual-feature summaries.
- Stage 3N admin-approved Discord HTML archive ingestion and source-discovery index.
- Stage 3O privacy-preserving Discord source promotion, expanded tutorials, and GitHub Wiki mirror source generation.
- Stage 3P deterministic image transform suite, contact sheets, and local visual review index.
- Stage 3Q redacted Discord AI-review bundles and topic shards.
- Stage 3R Discord lead promotion audit, negative controls, and first disabled post-Discord experiment manifests.
- Stage 3S bounded Onion 7 explicit seed-pack execution.
- Stage 3T bounded GP/rune claim verifier execution.
- Stage 3U bounded cookie SHA-256 signed-variant pack execution.
- Stage 3V OutGuess regression harness.
- Stage 3W project-state consolidation and anti-drift checks.
- Stage 3X CLI modularisation without behavior change.
- Stage 3Y result synthesis, staged plan, and method-retirement ledger.
- Stage 3Z source-of-truth / newcomer map.
- Stage 4A full Discord research-bundle extraction and static review site generation.
- Stage 4B website-derived source-lock triage and visual observation intake.
- Stage 4C cuneiform and dot annotation pack.
- Stage 4D bounded numeric verifier pack.
- Stage 4E cicada-solvers/iddqd source-lock delta audit.
- Stage 4F historical OutGuess/audio fixture source-locking.
- Stage 4G cookie exact-candidate refresh.
- Stage 4H CPU batch transform API extraction.
- Stage 4I scorer consolidation and calibration report.
- Stage 4J observation review workflow hardening.
- Stage 4K allowlisted public source-lock snapshots.
- Stage 4L reviewed observation promotion ledger.
- Stage 4M image source-variant and compression preflight.
- Stage 4N OutGuess/audio positive-control completion.
- Stage 4O CPU batch adapter expansion.
- Stage 4P result-store and score-summary unification.
- Stage 4Q CPU benchmark and parity planning.
- Stage 5A CUDA planning and parity scaffolding.
- Stage 5B CUDA parity harness skeleton.
- Stage 5C CUDA build and device-detection scaffold.
- Stage 5D native C++ CPU batch backend and deterministic threading baseline.
- Stage 5E first CUDA kernel contract and CPU/native parity adapter selection.
- Stage 5F first synthetic-only CUDA parity kernel implementation.
- Stage 5G-5O CUDA parity reporting, Gematria contract/preparation/kernel reporting, solved-fixture token mapping, exact solved-fixture parity, exact repeat verification, and compact result-store preflight.
- Stage 5G shift_score CUDA parity reporting and solved-fixture-safe adapter preflight.
- Stage 5H Gematria mod-29 shift_score contract and native parity fixture preparation.
- Stage 5I Gematria mod-29 shift_score synthetic CUDA parity preparation.
- Stage 5J Gematria mod-29 shift_score synthetic CUDA parity kernel implementation.
- Stage 5K Gematria shift_score CUDA parity reporting and solved-fixture-safe preflight.
- Stage 5L solved-fixture-safe Gematria shift_score token mapping and native parity fixture preparation.
- Stage 5M first solved-fixture-safe Gematria shift_score CUDA parity run.
- Stage 5N solved-fixture-safe Gematria CUDA parity reporting and controlled expansion gate.
- Stage 5O solved-fixture-safe Gematria CUDA repeat verification and result-store preflight.
- Stage 5P controlled solved-fixture CUDA result-store integration.
- Stage 5Q controlled expansion candidate mapping.
- Stage 5R controlled expanded solved-fixture-safe Gematria CUDA parity.
- Stage 5S expanded solved-fixture Gematria CUDA parity reporting and result-store integration.
- Stage 5T solved-family CUDA readiness matrix.
- Stage 5U Candidate Batch ABI contract consolidation.
- Stage 5V native Candidate Batch ABI conformance.
- Stage 5W prime-minus-one stream native parity contract preparation.
- Stage 5X prime-minus-one no-GPU native parity execution.
- Stage 5Y prime-minus-one native parity reporting and CUDA contract readiness.
- Stage 5Z prime-minus-one CUDA contract preparation.
- Stage 5AA prime-minus-one CUDA synthetic validation.
- Stage 5AB operational document staleness hardening.
- Stage 5AC prime-minus-one CUDA synthetic reporting and bounded-p56 preflight.
- Stage 5AD bounded p56 CUDA parity mismatch record.
- Stage 5AD-fix bounded p56 mismatch investigation.
- Stage 5AE corrected bounded p56 formula reporting and reference-contract repair.
- Stage 5AF Cicada source harvester and archive/visual/numeric provenance inventory tooling.
- Stage 5AG local third-party source inventory and initial source-lock metadata.
- Stage 5AH operational documentation staleness coverage repair and README stage-ledger audit.
- Stage 5AI curated research bundle extraction from local source inventory.
- Stage 5AM static research website renderer and webserver export package.
- Stage 5AN private Deep Research content pack and SFTP-ready hosted content library.
- Stage 5AR page 49-51 original-image pixel-coordinate and page-split source-gap closure.
- Stage 5AU token case-review pack usability fix and glyph-tight crop rebuild.
- Stage 5AV token case-review decision integration and compact variant-branch manifest.
- Stage 5AW decision possible-token parser cleanup and branch-manifest repair.
- Stage 5AX parallel validation harness and fast CI check orchestrator.
- Stage 5AY bounded token-block preflight manifest design without execution.
- Stage 5AZ bounded preflight manifest integrity gap closure.
- Stage 5BB token-block preflight runner scaffold without execution.
- Stage 5BD token-block preflight dry-run implementation without byte-stream generation.
- Stage 5BE Deep Research review of token-block preflight dry-run implementation, archive/evidence hygiene, and execution-gate enforcement.
- Stage 5BF historical route source-lock and technique extraction from local CicadaSolversIddqd archive metadata.
- Stage 5BI Fandom source-lock triage and original-archive crosswalk integration.
- Stage 5BJ original-archive crosswalk closure for high-priority Fandom-derived candidates.
- Stage 5BK historical-route planning constraint integration and iddqd-v2 source-lock addendum.
- Stage 5BM Deep Research findings integration and String 4 branch-crosswalk repair.
- Stage 5BN String 4 unsupported-position source-gap closure and inactive addendum metadata.
- Stage 5BO token-case human-review errata integration and inactive String 4 full-branch reclassification metadata.
- Stage 5BS inactive-branch planning-ingestion gate and future-runner citation policy.
- Stage 5BY inactive-sidecar planning manifest scaffold and no-execution planning-ingestion sidecar.
- Stage 5CA inactive-sidecar review contract hardening with exact citation, fail-closed trigger, activation-precondition, and manifest-supersession preflight contracts.
- Stage 5CC active-planning-input proposal preflight with Stage 5CB warning integration, Stage 5CA citation preservation, exact fail-closed trigger/precondition contracts, no-byte-stream and no-execution transition gates, Stage 5BD preservation, and active-lineage preservation.
- Stage 5CG post-review approval-gate integration with Stage 5CF warning integration, unsatisfied operator and Deep Research decision scaffolds, Stage 5CE proposal-package preservation, Stage 5CC contract preservation, Stage 5BD plan preservation, active-lineage preservation, and closed no-byte/no-execution gates.
- Stage 5CI approval-record template hardening with Stage 5CH warning integration, future operator approval and Deep Research acceptance templates, combined approval-gate validation preflight, activation-decision template, negative validation contract, Stage 5CG/5CE/5CC/5BD preservation, active-lineage preservation, and closed no-byte/no-execution gates.
- Stage 5CK approval-record validation fixture pack and activation-decision review package with Stage 5CJ warning integration, fixture-only operator/Deep Research/activation validation packs, negative-validation matrix, approval-gate non-satisfaction proof, Stage 5CI/5CG/5CE/5CC/5BD preservation, active-lineage preservation, and closed no-byte/no-execution gates.
- Stage 5CM approval-record readiness boundary and activation-decision gate hardening with Stage 5CL warning integration, fixture-vs-real boundary contracts, end-to-end readiness-boundary validation, future real approval-readiness preflight, credential-redaction policy, Stage 5CK/5CI/5CG/5CE/5CC/5BD preservation, active-lineage preservation, 8-worker validation cap, and closed no-byte/no-execution gates.
- Stage 5CO real approval-record readiness package and activation-decision transition planning with Stage 5CN warning integration, future operator/Deep Research/combined-gate/activation preflights, transition sequence, missing-requirements register, Stage 5CM/5CK/5CI/5CG/5CE/5CC/5BD preservation, active-lineage preservation, credential-redaction preservation, review-packaging warning, 8-worker validation cap, and closed no-active/no-byte/no-execution gates.
- Stage 5CU operator-decision option negative-fixture hardening with Stage 5CT warning integration, Stage 5CS readiness/options preservation, 41 decision-option negative fixtures, 13 option-selection misuse cases, real-record blockers, 8-worker validation cap preservation, and closed no-active/no-byte/no-execution gates.
- Stage 5CW real-decision package preflight with Stage 5CV warning integration, Stage 5CU negative-fixture preservation, Stage 5CS six-option preservation, 24 future real-decision inputs, 24 preflight misuse cases, 8-worker validation cap preservation, and closed no-active/no-byte/no-execution gates.

## Architecture summary

The CPU side owns corpus management, manifests, hypothesis generation, branching search, result provenance, and manual review. The GPU side will only accelerate large regular batches of transform-and-score work after a CPU reference implementation, parity tests, and benchmarks exist.

## Where To Start

- [Start Here](docs/onboarding/start-here.md): plain-English current-state overview.
- [Source Of Truth Map](docs/onboarding/source-of-truth-map.md): which file answers which question.
- [Staged Plan](docs/roadmap/staged-plan.md): completed stages, current direction, planned work, deferred work, and method-retirement context.
- [Tutorial Index](tutorials/README.md): public workflow guides.

## Current status

- Stage 2A: CPU transform registry and manifest-addressable solved-baseline runner complete.
- Stage 2B: JSONL/SQLite experiment result-store foundation complete.
- Stage 2C: raw-data-free GitHub Actions CI complete and lock-hash hardened.
- Stage 2D: CI-gated schema/docs consistency and manifest/result-store hardening complete.
- Stage 2E: CPU exploratory experiment manifest scaffold and dry-run planner complete.
- Stage 2F: bounded CPU execution harness for synthetic and solved-fixture-only runs complete.
- Stage 2G: exploratory experiment proposal and human-approval workflow complete.
- Stage 2H: approval-gated execution path for approved synthetic/solved controls complete.
- Stage 2I: first real bounded CPU exploratory experiment approval packet complete.
- Stage 2J: standing bounded CPU auto-run policy and queue scaffold complete.
- Stage 3A: minimal CPU Caesar plus affine executor and triage scoring complete.
- Stage 3B: Stage 3A lead inspection, scoring refinement, rerank, and reverse-direction comparison complete.
- Stage 3C: scoring calibration, null controls, positive controls, and tiny crib checks complete.
- Stage 3D: small Vigenere known-motif key-list preview complete.
- Stage 3E: Deep Research method backlog ingestion and bounded queue dry-run complete.
- Stage 3F: LP evidence-key Vigenere pack execution complete.
- Stage 3G: p56-local prime-minus-one offset sweep complete.
- Stage 3H: reset/advance ablation and family-specific negative controls complete.
- Stage 3I: historical motif Vigenere key-pack run complete.
- Stage 3J: Mersenne/perfect-number tiny stream probe complete.
- Stage 3K: archive and visual observation registry complete.
- Stage 3L: bounded cookie-hash preimage packs complete.
- Stage 3M: deterministic local image analysis complete.
- Stage 3N: admin-approved Discord HTML archive ingestion complete.
- Stage 3O: Discord source promotion and Wiki tutorial mirror complete.
- Stage 3P: deterministic image transform suite and visual review index complete.
- Stage 3Q: redacted Discord AI-review bundles and topic shards complete.
- Stage 3R: Discord lead promotion audit and first post-Discord manifest queue complete.
- Stage 3S: bounded Onion 7 explicit seed-pack execution complete.
- Stage 3T: bounded GP/rune claim verifier execution complete.
- Stage 3U: bounded cookie SHA-256 signed-variant pack execution complete.
- Stage 3V: OutGuess regression harness complete.
- Stage 3W: state consolidation and anti-drift hardening complete.
- Stage 3X: CLI modularisation without behavior change complete.
- Stage 3Y: result synthesis, staged plan, and method-retirement ledger complete.
- Stage 3Z: source-of-truth / newcomer map complete.
- Stage 4A: full Discord research-bundle extraction for Deep Research complete.
- Stage 4B: website-derived source-lock triage and visual observation intake complete.
- Stage 4C: cuneiform and dot annotation pack complete.
- Stage 4D: bounded numeric verifier pack complete.
- Stage 4E: cicada-solvers/iddqd source-lock delta audit complete.
- Stage 4F: historical OutGuess/audio fixture source-locking complete.
- Stage 4G: cookie exact-candidate refresh complete.
- Stage 4H: CPU batch transform API extraction complete.
- Stage 4I: scorer consolidation and calibration report complete.
- Stage 4J: observation review workflow hardening complete.
- Stage 4K: allowlisted public source-lock snapshots complete.
- Stage 4L: reviewed observation promotion ledger complete.
- Stage 4M: image source-variant and compression preflight complete.
- Stage 4N: OutGuess/audio positive-control completion complete.
- Stage 4O: CPU batch adapter expansion complete.
- Stage 4P: result-store and score-summary unification complete.
- Stage 4Q: CPU benchmark and parity planning complete.
- Stage 5A: CUDA planning and parity scaffolding complete.
- Stage 5B: CUDA parity harness skeleton complete.
- Stage 5C: CUDA build and device-detection scaffold complete.
- Stage 5D: native C++ CPU batch backend and deterministic threading baseline complete.
- Stage 5E: first CUDA kernel contract and CPU/native parity adapter selection complete.
- Stage 5F: first synthetic-only CUDA parity kernel implementation complete.
- Stage 5G: shift_score CUDA parity reporting and solved-fixture-safe adapter preflight complete.
- Stage 5H: Gematria mod-29 shift_score contract and native parity fixture preparation complete.
- Stage 5I: Gematria mod-29 shift_score synthetic CUDA parity preparation complete.
- Stage 5J: Gematria mod-29 shift_score synthetic CUDA parity kernel implementation complete.
- Stage 5K: Gematria shift_score CUDA parity reporting and solved-fixture-safe preflight complete.
- Stage 5L: solved-fixture-safe Gematria shift_score token mapping and native parity fixture preparation complete.
- Stage 5M: first solved-fixture-safe Gematria shift_score CUDA parity run complete.
- Stage 5N: solved-fixture-safe Gematria CUDA parity reporting and controlled expansion gate complete.
- Stage 5O: solved-fixture-safe Gematria CUDA repeat verification and result-store preflight complete.
- Stage 5P: controlled solved-fixture CUDA result-store integration complete.
- Stage 5Q: controlled solved-fixture-safe Gematria shift_score expansion candidate mapping complete.
- Stage 5R: controlled expanded solved-fixture-safe Gematria shift_score CUDA parity complete.
- Stage 5S: expanded solved-fixture Gematria CUDA parity reporting and result-store integration complete.
- Stage 5T: solved-family CUDA readiness matrix complete.
- Stage 5U: Candidate Batch ABI contract consolidation complete.
- Stage 5V: native Candidate Batch ABI conformance complete.
- Stage 5W: prime-minus-one stream native parity contract preparation complete.
- Stage 5X: prime-minus-one no-GPU native parity execution complete.
- Stage 5Y: prime-minus-one native parity reporting and CUDA contract readiness complete.
- Stage 5Z: prime-minus-one CUDA contract preparation complete.
- Stage 5AA: prime-minus-one CUDA synthetic validation complete.
- Stage 5AB: operational document staleness hardening complete.
- Stage 5AC: prime-minus-one CUDA synthetic reporting and bounded-p56 preflight complete.
- Stage 5AD: bounded p56 CUDA parity mismatch record complete.
- Stage 5AD-fix: bounded p56 mismatch investigation complete.
- Stage 5AE: corrected bounded p56 formula reporting and reference-contract repair complete.
- Stage 5AF: Cicada source harvester and archive/visual/numeric provenance inventory tooling complete.
- Stage 5AG: local third-party source inventory and initial source-lock metadata complete.
- Stage 5AH: operational documentation staleness coverage repair and README stage-ledger audit complete.
- Stage 5AI: curated research bundle extraction from local source inventory complete.
- Stage 5AJ: UsefulFilesAndIdeas local-source integration and extraction-fidelity policy complete.
- Stage 5AK: community-facts observations integration and number-fact claim curation complete.
- Stage 5AL: research website-ingest staging and Deep-Research export validation complete.
- Stage 5AM: static research website renderer and webserver export package complete.
- Stage 5AN: private Deep Research content pack and SFTP-ready hosted content library complete.
- Stage 5AP: page 49-51 token-block source-lock and OutGuess positive-control infrastructure complete.
- Stage 5AR: page 49-51 original-image coordinate lock complete.
- Stage 5AU: token case review-pack v2 usability fix complete.
- Stage 5AV: token case-review decision integration and compact variant-branch manifest complete.
- Stage 5AW: decision possible-token parser cleanup and branch-manifest repair complete.
- Stage 5AX: parallel validation harness and fast CI check orchestrator complete.
- Stage 5AY: bounded token-block preflight manifest design without execution complete.
- Stage 5AZ: bounded preflight manifest integrity gap closure complete.
- Stage 5BD: token-block preflight dry-run implementation without byte-stream generation complete.
- Stage 5BE: Deep Research review of token-block preflight dry-run implementation complete.
- Stage 5BF: historical route source-lock and technique extraction from local CicadaSolversIddqd archive metadata complete.
- Stage 5BI: Fandom source-lock triage and original-archive crosswalk integration complete.
- Stage 5BJ: original-archive crosswalk closure for high-priority Fandom-derived candidates complete.
- Stage 5BK: historical-route planning constraint integration and iddqd-v2 source-lock addendum complete.
- Stage 5BM: Deep Research findings integration and String 4 branch-crosswalk repair complete.
- Stage 5BN: String 4 unsupported-position source-gap closure and inactive addendum metadata complete.
- Stage 5BO: token-case human-review errata integration and inactive String 4 full-branch reclassification complete.
- Stage 5BS: inactive String 4 planning-ingestion gate, reviewable evidence metadata, and fail-closed future-runner citation policy complete.
- Stage 5BU: Stage 5BS lineage-path erratum, preserved active-lineage digest index, path-resolution validation, and validator hardening complete.
- Stage 5BY: inactive planning manifest scaffold, no-execution planning-ingestion sidecar, Stage 5BW duplicate source-digest classification, filename-equivalence map, active-lineage preservation, and Stage 5BD run-plan preservation complete.
- Stage 5CA: inactive-sidecar review contract, exact future-runner citation contract, fail-closed trigger contract, activation-precondition contract, manifest-supersession preflight contract, Stage 5BD preservation, active-lineage preservation, no-active-ingestion proof, and no-byte-stream proof complete.
- Stage 5CB: Deep Research review of Stage 5CA accepted the inactive-sidecar contract hardening with warnings and selected Stage 5CC active-planning-input preflight hardening without execution.
- Stage 5CC: active-planning-input proposal preflight, exact fail-closed trigger/precondition validation, no-byte-stream transition gate, no-execution transition gate, Stage 5BD preservation, active-lineage preservation, and DWH quarantine reaffirmation complete without activating String 4.
- Stage 5CG: post-review approval-gate integration, Stage 5CF findings integration, operator/Deep Research decision scaffolds, Stage 5CE wording review, no-byte/no-execution transition gates, Stage 5BD preservation, and active-lineage preservation complete without satisfying approvals, selecting or authorizing active input, or activating String 4.
- Stage 5CI: approval-record template hardening, Stage 5CH findings integration, future operator approval and Deep Research acceptance templates, combined approval-gate validation preflight, activation-decision template, negative validation contract, no-byte/no-execution transition gates, Stage 5BD preservation, and active-lineage preservation complete without creating approval records, satisfying the gate, selecting or authorizing active input, or activating String 4.
- Stage 5CK: approval-record validation fixture pack and activation-decision review package, Stage 5CJ findings integration, fixture-only operator approval, Deep Research acceptance, activation-decision, and negative-validation records, approval-gate non-satisfaction proof, no-byte/no-execution transition gates, Stage 5BD preservation, and active-lineage preservation complete without creating actual approval records, satisfying the gate, selecting or authorizing active input, or activating String 4.
- Stage 5CM: approval-record readiness boundary and activation-decision gate hardening, Stage 5CL findings integration, fixture-vs-real boundary records, end-to-end boundary validation, future real approval-readiness preflight, credential-redaction/no-secret policy, no-byte/no-execution transition gates, Stage 5BD preservation, and active-lineage preservation complete without creating real approval records, satisfying the gate, selecting or authorizing active input, or activating String 4.
- Stage 5CO: real approval-record readiness package and activation-decision transition planning, Stage 5CN findings integration, future real operator approval, Deep Research acceptance, combined-gate, activation-decision, missing-requirements, and transition-sequence metadata, no-active/no-byte/no-execution transition gates, Stage 5CM/5CK/5CI/5CG/5CE/5CC/5BD preservation, and active-lineage preservation complete without creating real approval records, satisfying the gate, selecting or authorizing active input, activating String 4, generating byte streams, or executing token-block work.
- Stage 5CW: operator-decision readiness review integration and real-decision package preflight complete with Stage 5CV findings integration, Stage 5CU negative-fixture preservation, Stage 5CS readiness/options preservation, 24 future real-decision inputs, 24 preflight misuse cases, Stage 5BD run-plan IDs unchanged, active lineage preserved, no real decisions or records created, and all no-active/no-byte/no-execution gates closed.
- Known solved baselines: `10` passing through the registry/manifest path.
- Fixture breakdown: direct translation `4`, Atbash-family `3`, explicit-key Vigenere `2`, p56 prime-minus-one / phi-prime `1`.
- Canonical corpus: inactive.
- Page boundaries: reviewable.
- Broad search/scoring/CUDA campaigns: not started.
- Historical CUDA kernel milestone: Stage 5J wrote `1` implementation record, `1` build record, `1` synthetic parity record, and `1` summary record for `gematria_mod29_shift_score_kernel`. Local optional CUDA build and synthetic numeric parity passed with hash `a6d5d5161145fd31ab429a8e955e0412d7b0af6089f06ee8b33baf8cd00b27a0`; no real Liber Primus CUDA data, solved or unsolved page CUDA execution, GPU benchmark, speedup claim, or solve claim was added.
- Historical Gematria solved-fixture CUDA reporting milestone: Stage 5N wrote `5` parity report records, `5` controlled expansion gate records, `1` boundary review record, `2` result-store/score-summary preflight records, `9` no-unsolved guardrail records, and `1` summary record. It carries forward Stage 5M parity pass/fail/skip `5/0/0`, approves only exact-repeat verification for Stage 5O, blocks broad solved-fixture and unsolved-page CUDA, adds `0` new CUDA kernels, modifies no CUDA source, runs no CUDA, and makes no benchmark, speedup, real Liber Primus CUDA-data, website-expansion, canonical-corpus, page-boundary, or solve claim.
- Latest solved-fixture mapping stage: Stage 5L wrote `5` token-mapping records, `5` native parity records, `1` output-hash contract, `1` score-summary shape, and `1` summary record. It maps all `5` candidate streams, prepares `5` native output-token hashes, and supplies Stage 5M's exact approved input set.
- Latest bounded hash review: Stage 4G tested `4` source-backed deduplicated SHA-256 candidate byte strings against the two archived cookie/hash targets for `8` exact comparisons and found `0` exact matches; no solve claim.
- Latest image-analysis stage: Stage 3M analysed `58` ignored local page images, producing `406` component records, `58` symmetry records, `464` bitplane records, and `71` review-only feature candidates in ignored outputs. No OCR, AI/ML interpretation, image-derived search, or solve claim is made.
- Latest source-discovery stage: Stage 3O promoted `500` public source links, `200` method-claim candidates, and `200` numeric-observation candidates from the Stage 3N extraction into redacted review records. It rejected private/unsafe links, expanded public tutorials, and generated Wiki source pages. Raw Discord logs, message bodies, usernames, private URLs, and generated review indexes remain uncommitted; no solve claim.
- Latest visual review stage: Stage 3P processed `58` ignored local page images, emitted `2077` derived review images, `59` contact sheets, `58` review pages, and `6` review-only visual transform candidates under ignored outputs. No OCR, AI/ML interpretation, image-derived search, or solve claim is made.
- Latest Discord review stage: Stage 3Q generated `1700` redacted stream records, `17` topic shard files, and `900` review leads under ignored outputs, with an aggregate-only committed summary. Raw logs, message bodies, usernames, private URLs, AI upload, live API use, scraping, and solve claims remain absent.
- Latest Discord promotion stage: Stage 3R promoted `13` public source records and `11` review-only observation records, preserved `11` negative-control records, counted `25` unsafe/private or quarantined records, and created `3` disabled post-Discord manifests. No experiment was executed and no solve claim was made.
- Latest post-Discord experiment stage: Stage 3S executed `EXP-3R-003` only, producing `72` bounded Onion 7 candidates from `3` value spaces, `6` routes, `2` directions, and `2` reset modes. The top candidate scored `1.460714` with calibrated confidence `inconclusive`; generated outputs remain ignored and no solve claim is made.
- Latest GP/rune verifier stage: Stage 3T executed `EXP-3R-004` only, loading and deduplicating `25` exact claims. It classified `23` as verified and `2` as unsupported, with no unverified, boundary-sensitive, missing-source-span, malformed, or duplicate claims in the committed input set.
- Latest cookie signed-variant stage: Stage 3U executed `EXP-3R-001` only, generating `156` candidates before deduplication, testing `105` deduplicated byte strings against `2` cookie targets for `210` exact SHA-256 comparisons, and finding `0` exact matches.
- Latest stego regression stage: Stage 3V added the OutGuess harness, detected no local OutGuess binary, and recorded `6` missing-tool skips plus `1` disabled case across `7` manifest cases. No raw artefacts or payloads were committed.
- Latest consolidation stage: Stage 3W refreshed persistent project context, defined the source-of-truth hierarchy, and added anti-drift checks so long-lived docs cannot drift back to obsolete current-state claims.
- Latest maintainability stage: Stage 3X split the Python CLI into `cli_commands` domain modules while preserving `python -m libreprimus.cli` and adding command-surface tests.
- Latest synthesis stage: Stage 3Y added `docs/roadmap/staged-plan.md`, research synthesis records, method-family status and retirement ledgers, Deep Research influence records, direction-change records, and validation CLI commands.
- Latest onboarding stage: Stage 3Z added source-of-truth, Codex navigation, Deep Research handoff, contributor module, task-lane, and private/generated data maps.
- Latest Deep Research handoff stage: Stage 4A processed `43` local ignored Discord HTML exports into `520009` redacted messages, `1327` channel shards, `12` topic shards, and an ignored SFTP-ready static review site with `58` LP page images included as generated gallery assets. Raw logs, raw images, private URLs, and generated outputs remain uncommitted.
- Latest source-lock stage: Stage 4B promoted `20` allowlisted public source records, recorded `19` source-health records, added `6` review-only visual observations and `17` negative controls, and queued `7` disabled future manifests. No experiments were executed and no solve claim is made.
- Latest annotation stage: Stage 4C created `15` visual annotation tasks, including `1` cuneiform task, `1` dot task, `2` delimiter tasks, and `10` visual negative-control tasks. Generated annotation outputs remain ignored and no visual meaning is inferred.
- Latest bounded numeric stage: Stage 4D discovered `7` manifests, audited `3`, deferred or skipped `4`, verified `0` GP/rune claims because no exact new spans were present, audited `2` delimiter observations and `10` visual negative controls, skipped number-square routes because raw values are not locked, and deferred cuneiform/cookie execution.
- Latest source-delta stage: Stage 4E inspected `310` public `cicada-solvers/iddqd` tree paths, recorded `1` source-delta record, `12` source-health records, `1` image artefact future-preflight record, and `4` disabled future manifests without committing raw artefacts.
- Latest stego/audio fixture stage: Stage 4F recorded `5` OutGuess fixture source records, `5` audio fixture source records, `10` source-health records, `5` toolchain requirement records, and `4` disabled future manifests without running OutGuess, OpenPuff, MP3Stego, hexdump/strings, audio analysis, or committing raw artefacts.
- Latest cookie refresh stage: Stage 4G generated `4` source-backed candidates before and after deduplication, marked `2` previous-pack duplicates, ran `8` SHA-256 exact comparisons, and found `0` exact matches without fuzzy matching, hashcat, GPU/CUDA, raw Discord processing, raw page-image processing, or solve claims.
- Latest CPU batch API stage: Stage 4H executed `6` synthetic CPU-only candidates, supported all `6` current registry transforms, wrote `6` ignored result records, and created the CPU/CUDA parity contract without GPU code.
- Latest scorer consolidation stage: Stage 4I recorded `3` scorer records, `9` confidence labels, `11` compatibility mappings, and `1` calibration profile. Positive/null/negative controls are available, CPU batch score compatibility is true, and scoring remains triage only.
- Latest observation review stage: Stage 4J loaded `96` observation-family records, wrote `96` review decisions, `96` promotion-gate records, `23` quarantine records, and promoted `0` observations to manifests. Review-only observations remain non-seeds.
- Latest source snapshot stage: Stage 4K considered `43` source candidates, wrote `15` allowlisted source-lock snapshot records, locked `8` GitHub commit-addressed references, fetched `1` ignored local snapshot, committed `0` raw snapshots, rejected `22` unsafe/noisy or non-priority sources, and recorded `6` duplicate sources.
- Latest observation promotion stage: Stage 4L loaded `97` reviewed observations, created `97` ledger records, `97` readiness records, `115` blocker records, and `13` manifest-readiness records. It marked `0` observations ready for manifest execution, `17` control-only, `14` source-reference-only, `48` blocked, `2` deferred, `15` quarantined, and `1` rejected. The added bigram/Fibonacci-421 community claim remains blocked pending reproducible matrix regeneration, rune-order declaration, indexing convention, null controls, and multiple-testing controls.
- Latest image preflight stage: Stage 4M scanned `58` ignored local LP page images, wrote `58` source-variant records, `58` deterministic compression metric records, `1` review-only image artifact candidate, and `1` blocked bigram/Fibonacci-421 readiness record. It committed no raw images or generated visualisations and ran no image/bigram experiment.
- Latest stego/audio readiness stage: Stage 4N wrote `11` OutGuess readiness records, `5` audio readiness records, `16` fixture-cache records, `16` expected-output records, `7` toolchain readiness records, `0` historical execution-ready fixtures, `8` blocked historical fixtures, and `2` synthetic-ready controls. It committed no raw artefacts or extracted payloads and ran no stego/audio tools.
- Latest result-store unification stage: Stage 4P recorded `18` source inventory records, loaded `11` committed summaries, saw `6` optional ignored generated outputs locally, wrote `82` unified result records, `82` unified score-summary records, and `82` method-status joins. It ran no new experiments, added no scorer semantics, committed no generated result bodies or SQLite databases, and added no CUDA code.
- Latest CUDA planning stage: Stage 5A wrote `14` target-plan records, `9` ready planning targets, `2` blocked targets, `8` explicit non-target records, `9` parity scaffold records, and `10` satisfied implementation gates. It made no CUDA source change, GPU benchmark, speedup claim, broad experiment, raw-data processing, or solve claim.
- Latest CUDA parity harness stage: Stage 5B wrote `14` harness plan records, `14` parity fixture records, `3` backend capability records, and `9` future-kernel matrix records. It made no CUDA source change, GPU benchmark, speedup claim, broad experiment, raw-data processing, or solve claim.
- Historical CUDA build/device milestone: Stage 5C wrote `3` build profiles, `3` toolchain records, `3` device records, and `1` optional smoke-build record. It made no CUDA source change, CUDA kernel, GPU benchmark, speedup claim, broad experiment, raw-data processing, website expansion, or solve claim.
- Historical native CPU backend milestone: Stage 5D wrote `1` backend capability record, `5` threading records, `1` native/Python parity record, and `1` diagnostic record. It tested thread counts `1,2,4,8,16`, produced matching one-thread and multi-thread hashes, preserved Python as orchestration, and made no CUDA source change, GPU benchmark, speedup claim, broad experiment, raw-data processing, website expansion, or solve claim.
- Historical CUDA reporting milestones: Stage 5G reports the Stage 5F `shift_score_kernel` native/CUDA synthetic hash match and Stage 5K reports the Stage 5J Gematria CUDA/native synthetic hash match. Both verify CUDA-facing device-code subset policy, record solved-fixture-safe blockers, and keep real Liber Primus CUDA data use, GPU benchmarks, speedup claims, broad execution, raw-data processing, website expansion, and solve claims out of scope.
- Historical Gematria CUDA kernel milestone: Stage 5J implements `gematria_mod29_shift_score_kernel` for the Stage 5H synthetic numeric fixture only. It shifts transformable tokens with `(token + shift) % 29`, preserves masked separator placeholders, matches the native fixture hash `a6d5d5161145fd31ab429a8e955e0412d7b0af6089f06ee8b33baf8cd00b27a0`, keeps Stage 5F uppercase Latin parity separate, and adds no real Liber Primus CUDA data use, solved/unsolved page CUDA execution, GPU benchmark, speedup claim, website expansion, or solve claim.
- Historical Gematria solved-fixture CUDA parity/reporting milestone: Stage 5N reports Stage 5M's five CUDA/native hash matches, records controlled expansion gates, and keeps unsolved-page CUDA blocked.
- Durable staged plan: [`docs/roadmap/staged-plan.md`](docs/roadmap/staged-plan.md).
- Latest Gematria expanded solved-fixture CUDA reporting stage: Stage 5S consumed the `3` Stage 5R expanded parity records, wrote `3` compact parity-report records, `3` result-store integration records, `3` score-summary integration records, `7` method-status impact records, `4` generated-body policy records, `1` boundary review record, and `6` controlled next-step decision records. It ran no CUDA, modified no CUDA source, added `0` kernels, published no generated CUDA result bodies, upgraded no method family to solved, and made no benchmark, speedup, unsolved-page CUDA, real Liber Primus CUDA-data, website-expansion, canonical-corpus, page-boundary, or solve claim.
- Latest prime-minus-one native contract stage: Stage 5W wrote `7` source inventory records, `2` stream contract records, `3` prime schedule records, `3` Candidate Batch ABI mapping records, `3` native parity preparation records, `3` result-store preflight records, `6` guardrail records, and `8` next-stage decision records. It marks the bounded Stage 4O/5L p56 mapping ready for future no-GPU native parity, keeps full p56 parity blocked until a complete committed token buffer is scoped, ran no CUDA or native/CUDA CMake, added no kernels, benchmarked nothing, and selected Stage 5X.
- Latest prime-minus-one native parity stage: Stage 5X wrote `3` native run records, `3` native parity records, `3` result-store preflight records, `3` score-summary preflight records, `1` full-p56 blocker record, `7` guardrail records, and `9` next-stage decision records. It executed only the two Stage 5W ready no-GPU Python-reference mappings, matched both Stage 5W expected hashes, skipped the blocked full p56 mapping, ran no CUDA or native/CUDA CMake, added no kernels, benchmarked nothing, and selected Stage 5Y.
- Latest source-harvester/website stage: Stage 5AN builds a private Deep Research content pack and SFTP-ready hosted content library from Stage 5AL/5AM metadata. It writes compact records under `data/deep-research-export/`, generated private pack files under `deep-research-content-packs/stage5an/`, hosted private content under `website-export/stage5an/private-content/`, and a combined upload root under `website-export/stage5an/webserver-root/`. It records `208` content-pack files, `211` hosted-content files, `10` bundles, `61` source records, `58` content records, `12` community-claim records, `183` private extracts, `7` publication gates, and `0` public website-ready records. It commits only metadata/contracts/scaffolds and performs no network fetch, online clone, Google Drive storage, raw source commit, public website publication, Deep Research execution, hypothesis generation/execution, OCR, AI/ML interpretation, image/stego/audio execution, CUDA, benchmark, scored experiment, or solve claim.
- Latest historical-route/token-block approval-readiness stage: Stage 5CW consumes Stage 5CV findings as compact metadata, preserves Stage 5CU negative fixtures and Stage 5CS readiness/options records plus Stage 5CQ and Stage 5CO readiness/transition records, creates a review-only real-decision package preflight, preserves 8 active-lineage paths and 10 Stage 5BD run-plan IDs, caps local validation at 8 workers, and leaves String 4 active input, dry-run ingestion, byte-stream generation, active-planning authorization, approval-gate satisfaction, activation authorization, and future token-block execution blocked.
- Latest validation stage: Stage 5AX adds opt-in parallel validation infrastructure with `10` parallel-safe commands, `6` serial commands, `1` blocked command, separated logs, failure aggregation, and safety audits while keeping git/GitHub/network/generated-output-writing operations serial. Stage 5CW preserves the local parallel-validation and pytest cap at 8 workers for Stage 5CM and later.
- Latest doc-staleness stage: Stage 5AH repairs README stage-ledger coverage, operational-file-map coverage, and current/next-stage consistency checks before curated extraction. Stage 5CW updates current/next-stage records to Stage 5CW complete and Stage 5CX next.
- Next: Stage 5CX - Deep Research review of Stage 5CW operator-decision readiness integration and real-decision package preflight, without execution.

## How To Use This Repo

1. Set up Python 3.12 and a local virtual environment using the [Windows](tutorials/02-windows-setup.md) or [Linux](tutorials/03-linux-setup.md) tutorial.
2. Run the local validation stack before trusting a change:

```powershell
.\.venv\Scripts\python.exe -m ruff check python/libreprimus tests/python
.\.venv\Scripts\python.exe -m pytest -q tests/python
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-state-drift
.\.venv\Scripts\python.exe -m libreprimus.cli research-synthesis validate --data-dir data/research --staged-plan docs/roadmap/staged-plan.md
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-all --allow-warnings
```

3. Keep local raw material local. Raw Discord logs, page images, transcript drops, workbooks, and Pastebin files are ignored by design.
4. Use generated outputs for local review only. Candidate dumps, image-analysis records, Discord extraction JSONL, SQLite databases, and local review indexes must not be committed.
5. Start with the [tutorial index](tutorials/README.md) for repo tours, solved baselines, bounded queues, image analysis, Discord archive ingestion, and source/observation registry workflows.
6. The GitHub Wiki mirrors tutorial pages for public browsing, but repository tutorial files are the source of truth.

Safe bounded CPU experiments use `experiments/policies/operator-policy-v0.yaml`; they remain CPU-only, budget-limited, and unable to claim solves. CUDA work waits for CPU references, parity tests, and explicit future scope.

## CI status

GitHub Actions runs at [NoxxGames/LiberPrimus-GPU Actions](https://github.com/NoxxGames/LiberPrimus-GPU/actions). CI is raw-data-free, CUDA-free, secret-free, and does not upload generated corpus or result artifacts by default. Real-source smoke checks remain local-only because ignored raw sources are not present on GitHub-hosted runners.

## Tutorials

Start with `tutorials/README.md`. The tutorials cover Windows and Linux setup, local data handling, current CLI tools, transcript alignment, hardware expectations, and Codex-assisted development.

## GitHub wiki

Wiki source pages live under `docs/wiki-source/` and are generated from `tutorials/`. The repository tutorials and docs are the source of truth; the GitHub wiki is a public mirror and must not contain raw data, generated dumps, or solve claims. Use `scripts/github/validate-wiki-source.ps1` and `scripts/github/sync-tutorials-to-wiki.ps1 --DryRun` before publishing.

## Issues and backlog

Issue templates live under `.github/ISSUE_TEMPLATE/`. Seed issues for future work live under `docs/github/issues/` and can be created idempotently with `scripts/github/create-issues.ps1`.

## Public-readiness status

The project is public-readable for documentation and scaffold review. It is not ready for unsolved-page cryptanalysis campaigns, canonical corpus release, or GPU acceleration claims.

## Quick start on Windows

```powershell
.\scripts\verify-toolchain.ps1
.\scripts\configure-windows.ps1
cmake --build build\msvc-debug
ctest --test-dir build\msvc-debug --output-on-failure
```

For Python:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip setuptools wheel
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\libreprimus.exe smoke
```

## Toolchain requirements

- Windows 11 or compatible Windows 10 development host.
- Git for Windows.
- CMake 3.26 or newer.
- Ninja.
- Python >=3.12,<3.14, with Python 3.12 preferred.
- Visual Studio 2022 Build Tools with the Desktop C++ workload.
- Optional CUDA Toolkit for CUDA smoke builds.

## Configure and build CPU-only

```powershell
cmake -S . -B build\msvc-debug -G Ninja -DCMAKE_BUILD_TYPE=Debug -DLPGPU_ENABLE_CUDA=OFF -DLPGPU_BUILD_TESTS=ON
cmake --build build\msvc-debug
ctest --test-dir build\msvc-debug --output-on-failure
```

If `cl.exe` is not visible in the current shell, run through `scripts\configure-windows.ps1`, which locates `VsDevCmd.bat`.

## Configure and build with CUDA

CUDA builds remain optional and are scaffold/smoke only at the current stage.

```powershell
cmake -S . -B build\cuda-debug -G Ninja -DCMAKE_BUILD_TYPE=Debug -DLPGPU_ENABLE_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=89 -DLPGPU_BUILD_TESTS=ON
cmake --build build\cuda-debug
ctest --test-dir build\cuda-debug --output-on-failure
```

## Python environment setup

The Python package exposes smoke/toolchain commands plus legacy ingestion, transcript alignment, profile validation, corpus-candidate generation, and solved-fixture reproduction.

Direct fixture smoke:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli solved-fixture stage1a-smoke --fixture-dir data/fixtures/solved-pages/direct-translation-v0 --candidate-dir data/normalized/corpus-candidates/rtkd-master-v0-candidate --out-dir data/normalized/solved-baselines/direct-translation-v0 --allow-pending --allow-warnings
```

All-known solved-baseline registry smoke:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli solved-baseline stage2a-smoke --manifest experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml --out-dir experiments/results/solved-baselines/stage2a --allow-warnings
```

Stage 2B result-store smoke:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli result-store stage2b-smoke --solved-baseline-manifest experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml --result-store-manifest experiments/manifests/result-store/stage2b-solved-baseline-import.yaml --solved-baseline-out-dir experiments/results/solved-baselines/stage2a --result-store-out-dir experiments/results/result-store/stage2b --replace --allow-warnings
```

Local Stage 2C CI reproduction:

```powershell
.\scripts\ci\run-python-ci.ps1
.\scripts\ci\run-schema-manifest-checks.ps1
```

## Repository map

- `src/`: C++20 native scaffold.
- `cuda/`: optional CUDA smoke scaffold.
- `python/`: Python orchestration package.
- `tests/`: C++ and Python smoke tests.
- `data/`: immutable raw-data placeholders and future corpus areas.
- `experiments/`: manifest-driven experiment policy and smoke manifest.
- `docs/`: methodology, CUDA, corpus, scoring, and Codex notes.
- `scripts/`: Windows verification, bootstrap, configure, cleanup, and GitHub helper scripts.
- `tutorials/`: public user-facing tutorials.
- `.github/`: issue templates and pull request template.

## Data policy

`data/raw/` is immutable. Do not overwrite raw evidence, normalize in place, or commit real raw corpus files. Corpus work must use explicit SHA-256 locks and transcript version metadata.

## Experiment policy

Experiments are manifest-driven. Candidate outputs must never be treated as solves without pinned corpus data, full transform chains, score metadata, null controls, reproducible tests, and manual review.

## Testing policy

Current tests cover the C++ skeleton, Python package, manifests, schemas, result stores, lock hashes, public documentation status, and consistency gates. Future CUDA kernels must have CPU reference implementations, CPU/GPU parity tests, and benchmarks before optimization.

## Next milestones

Historical snapshot: early milestones after Stage 2J.

Stage 2J replaced per-experiment approval as the default path with the standing policy in `experiments/policies/operator-policy-v0.yaml` and the queue in `experiments/queues/stage2j-bounded-cpu-queue.yaml`. Normal local CPU items can run automatically when they stay within the hard limits: candidate upper bound `100000`, runtime estimate `600` seconds, generated output budget `250` MB, CPU only, no CUDA/cloud/paid services, no generated-output commit, no canonical corpus activation, no page-boundary finalization, and no solve claim.

The first Caesar plus affine reviewable-slice queue item has candidate upper bound `841` and is policy-eligible. Stage 3A adds the minimal CPU executor and deterministic triage scoring for that item. Full candidate outputs remain ignored under `experiments/results/bounded-auto-runs/stage3a/`; committed research logs summarize counts and top score metadata only.

Stage 3B inspected Stage 3A top candidates, refined the scorer, reranked the 841 candidates, and ran the reverse-direction comparison. Both refined and reverse-direction top leads remain `noisy`.

Stage 3C calibrated scoring against positive solved-fixture controls, deterministic null controls, negative controls, and tiny crib checks. Stage 3D ran the conservative small Vigenere known-motif key-list preview for exactly four declared keys. The top key was `LIBER`, calibrated as `noisy`.

Stage 3E ingests the Deep Research method backlog, commits `experiments/queues/stage3e-method-backlog.yaml` and `experiments/queues/stage3e-bounded-cpu-queue.yaml`, and dry-runs bounded methods with deterministic counts: LP evidence Vigenere `48`, p56 local prime-minus-one offsets `256`, historical Vigenere `56`, family-specific negative controls `100`, reset/advance ablation `64`, prime mod/gap `256`, and Mersenne/perfect-number probe `192`.

Stage 3F implements the reset/advance-aware evidence-key Vigenere pack executor and runs only `stage3e_vig_lp_evidence_pack_v1`. It executes `48` candidates, records key/reset/advance metadata, leaves generated outputs ignored, and makes no solve claim.

Stage 3G implements the p56-local prime-minus-one offset sweep executor and runs only `stage3e_prime_minus_one_offsets_v1`. It executes `256` candidates, records offset/direction/reset metadata, leaves generated outputs ignored, adds a future `192` candidate Mersenne/perfect-number probe to the queue without executing it, and makes no solve claim.

Stage 3H implements the shared reset/advance state machine and runs only `stage3h_reset_advance_ablation_v1`. It executes `64` bounded candidates across Vigenere and prime-stream adapters, records reset/advance and metadata-support status, writes `100` ignored family-specific negative controls, and makes no solve claim.

Stage 3I reuses the bounded Vigenere key-pack executor and runs only `stage3e_vig_history_key_pack_v1`. It executes `56` candidates for the 14 declared historical motif keys across reset modes `none` and `line` and advance modes `runes_only` and `token_break_preserving`. The top key `SELFRELIANCE` remains calibrated `noisy`; generated outputs stay ignored and no solve claim is made.

Stage 3J implements the bounded Mersenne/perfect-number stream probe and runs only `stage3j_mersenne_prime_stream_tiny_v1`. It executes `192` candidates from the finite declared exponent sequence, reports `96` duplicate stream signatures, leaves generated outputs ignored, and makes no solve claim.

## Stage 1B Atbash-Family Fixtures

The workbench now includes known-solved reverse Gematria and rotated reverse Gematria reproduction fixtures. These run through:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli solved-fixture stage1b-smoke `
  --direct-fixture-dir data/fixtures/solved-pages/direct-translation-v0 `
  --atbash-fixture-dir data/fixtures/solved-pages/atbash-family-v0 `
  --candidate-dir data/normalized/corpus-candidates/rtkd-master-v0-candidate `
  --direct-out-dir data/normalized/solved-baselines/direct-translation-v0 `
  --atbash-out-dir data/normalized/solved-baselines/atbash-family-v0 `
  --allow-pending `
  --allow-warnings
```

These fixtures are regression baselines, not new solve claims. Generated outputs remain ignored, and `canonical_corpus_active=false`.
## Stage 1C Vigenere Baselines

Stage 1C adds explicit-key Vigenere known-solved fixture reproduction for `DIVINITY` and `FIRFUMFERENFE`, plus reference-source locks for selected `scream314/cicada3301` and `lipeeeee/gematria` files. These are provenance and test fixtures only: no new page is solved, no key search is implemented, and `canonical_corpus_active=false` remains required.

## Stage 1D Prime-Stream Baseline

Stage 1D adds p56 `An End` known-solved reproduction using a CPU-only `prime_minus_one_stream` transform with `phi_prime_stream` recorded as an equivalent alias for prime inputs. The p56 hex block is preserved as a payload check, not merged into plaintext. No prime-stream search, scoring, CUDA, or corpus activation is implemented.

## Stage 2B Result Store

Stage 2B adds generated JSONL and SQLite result stores for solved-baseline regression imports. Run records preserve manifest SHA-256, registry SHA-256, git commit, profile/source provenance, and explicit false flags for canonical corpus activation, page-boundary finalization, search, scoring, CUDA, and canonical trust. Generated result-store outputs under `experiments/results/result-store/` remain ignored and are not publication artifacts.

## Stage 2C CI

Stage 2C adds `.github/workflows/ci.yml` plus local scripts under `scripts/ci/`. CI is raw-data-free, CUDA-free, secret-free, and does not upload generated corpus or result artifacts by default. The Python job runs Ruff, pytest, package smoke, transform-registry validation, solved-baseline manifest validation, and result-store manifest validation.
