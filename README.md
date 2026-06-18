# liberprimus-gpu

[![CI](https://github.com/NoxxGames/LiberPrimus-GPU/actions/workflows/ci.yml/badge.svg)](https://github.com/NoxxGames/LiberPrimus-GPU/actions/workflows/ci.yml)

## Mission

`liberprimus-gpu` is a reproducible research workbench for conservative Liber Primus cryptanalysis experiments. The project keeps corpus provenance, solved baselines, transform metadata, run records, and CI gates ahead of any exploratory search or GPU acceleration work.

## Current boundaries and deferred work

Current completed stage: Stage 6H - Current-state integrity repair and dot-angle / right-triangle number-triangle source-lock addendum, without execution.

Current next prompt: Stage 6I - Final finite Stage 7 probe manifest and archive-run contract, without execution.

Stage 6H repairs Stage 6G current-state and doc-staleness misses, source-locks dot-angle/right-triangle/PDD153 review metadata, creates required Source Browser overlays, and hands explicit inputs to Stage 6I. Stage 6H created no final Stage 7 manifest, archive, probe execution, route stream, byte stream, target selection, image interpretation, or solve claim.

These are not permanent project exclusions. CUDA and broad campaigns are deferred, not permanently excluded.

### Permanent safety rules

No generated output is a solve by itself. No Liber Primus page is claimed solved unless a future reproducible manifest and matching output prove it. Any page still unsolved must not receive a solve claim.

### Current boundaries

- Canonical corpus: inactive.
- Page boundaries: reviewable.
- Broad unsolved-page search campaigns: not started.
- Scoring campaigns: not started; Stage 3A/3B minimal triage scoring exists only for sorting and inspecting bounded 841-candidate CPU runs, Stage 3C calibration uses small local controls only, Stage 3D applies that scorer to a four-key explicit Vigenere preview only, Stage 3F applies it to the bounded 48-candidate LP evidence-key Vigenere pack only, Stage 3G applies it to a bounded 256-candidate p56-local prime-minus-one offset sweep only, Stage 3H applies it to a bounded 64-candidate reset/advance ablation with 100 negative controls only, Stage 3I applies it to a bounded 56-candidate historical motif Vigenere pack only, Stage 3J applies it to a bounded 192-candidate Mersenne/perfect-number stream probe only, and Stage 3S applies it to the bounded 72-candidate Onion 7 explicit seed pack only.
- Cookie/hash preimage work: Stage 3L tests two explicit SHA-256 packs only.
- Visual/image-derived observations: registry and deterministic feature summaries only.
- CUDA experiment campaigns: not started.

### Deferred future work

CUDA kernels after CPU references and parity tests exist. Broad search/scoring/CUDA campaigns: not started.

### Already implemented since Stage 0A

Stage 3X CLI modularisation completed without behavior change. Stage 5AE corrected formula-parity reporting repaired the bounded p56 hash lineage while preserving Stage 5AD as historical failed parity.

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
- Stage 5CY: operator-facing option-selection decision preflight complete with Stage 5CX findings integration, Stage 5CW preflight preservation, Stage 5CW pytest-count reconciliation, Stage 5CU negative-fixture preservation, Stage 5CS exact six-option preservation, Stage 5BD run-plan IDs unchanged, active lineage preserved, no option selected, no real decisions or records created, and all no-active/no-byte/no-execution gates closed.
- Stage 5DE: real operator approval preparation package complete with Stage 5DD / assistant review context integration, Stage 5DC selected option `prepare_real_operator_approval_record` preserved, review-label anomaly recorded as non-gate-opening, 34 future approval-record requirements, Stage 5BD run-plan IDs unchanged, active lineage preserved, no real approval/acceptance/gate/activation/active-input records created, and all no-active/no-byte/no-execution gates closed.
- Stage 5DG: real operator approval record creation complete with Stage 5DF assistant/operator review context integration, Stage 5DE preparation package preserved, Stage 5DC selected option preserved, one valid operator approval record created, operator approval component satisfied, Deep Research acceptance absent, combined gate unsatisfied, activation unauthorized, active input unselected, Stage 5BD run-plan IDs unchanged, active lineage preserved, and all no-active/no-byte/no-execution gates closed.
- Stage 5DJ: CicadaMusic source-lock and music-clue pivot integration complete with 7 local ignored CicadaMusic files hashed, 4 MP3 metadata records, 3 PDF metadata records, 1 music candidate family, 7 unselected pivot options, Stage 5DG operator approval preserved, Stage 5BD run-plan IDs preserved at 10, active lineage preserved at 8, Deep Research acceptance absent, combined gate unsatisfied, activation unauthorized, byte streams blocked, execution blocked, target validation absent, Tor/network access absent, audio stego blocked, and no solve claim.
- Stage 5DK: Fandom source-lock gap closure and Page 56 hash-contract refinement complete with 14 Fandom sources recorded, corrected source-index crosswalks, Stage 5DI/Page 56 locks reused where applicable, 1 speculative source quarantined, the Page 56 512-bit hash preserved with unknown algorithm/preimage, 8 active-lineage records preserved, 10 Stage 5BD run-plan IDs preserved, all pivot options unselected, target validation absent, Tor/network access absent, DWH/hash/preimage search absent, byte streams blocked, execution blocked, and no solve claim.
- Stage 5DL: triangle / disk / quote / koan source-lock refresh complete with local NumberTriangleStuff, DiskCipherStuff, RedditStuff, quote-dialogue crib, and koan-page metadata recorded, 10 candidate families added or updated, `pdd_153_triangle_word_prime_route_v1` recorded as a future operator preference only, 8 active-lineage records preserved, 10 Stage 5BD run-plan IDs preserved, no target selected, target validation absent, Tor/network access absent, DWH/hash/preimage search absent, byte streams blocked, execution blocked, and no solve claim.
- Stage 5DM: visual-route source-lock addendum complete with 8 addendum families recorded, Blake visual-text context, Sacred Book overlay metadata, Page6 magic-square word/number precedent, full-page visual motif index, Page32 Moebius/Fibonacci-prime-index arithmetic, doublet-scarcity feature planning, evidence-atlas readiness, and Drive/path aliases. Stage 5DM preserves Stage 5DL, selects no target, performs no OCR/image forensics/route extraction/byte-stream generation/execution, and makes no solve claim.
- Stage 5DN: DiskCipher v1 source-lock and triangle/circumference bridge update complete with 27 DiskCipherStuff files inventoried, updated `message_bodies.txt` and `results.png` source locks, 11 candidate bridge records, probability-claim quarantine, Stage 5DG/Stage 5BD/active-lineage preservation, no target selected, no Alberti/disk-cipher or HTML execution, no OCR/image forensics, no byte-stream generation, no CUDA, and no solve claim.
- Stage 5DO: Discord NumberFacts and pixel-colour source-lock addendum complete with 11 NumberFactsCollection files, 10 PotentialHint files, two `messages.txt` source locks, image-anchor line hashes, 15 review-only candidate records, canonical transcript/image blockers, future source-lock browser GUI requirements, Stage 5DN preservation, Stage 5DG/Stage 5BD/active-lineage preservation, no target selected, no GUI puzzle execution, no OCR/image forensics, no byte-stream generation, no CUDA, and no solve claim.
- Stage 5DP: New Reddit Mayfly / dot / cover / ISO source-lock addendum complete with 9 RedditStuff source folders, 6 required folders represented, Mayfly docx/xlsx source locks, Mayfly `958x1092` and `230x262` workbook metadata, 23 review-only candidate/crosslink records, ChatGPT context file update, Stage 5DO preservation, Stage 5DG/Stage 5BD/active-lineage preservation, no target selected, no GUI implementation, no route extraction, no OCR/image forensics, no byte-stream generation, no CUDA, and no solve claim.
- Stage 5DQ: Operator Console v0 Source Browser complete with `1293` review-only source-browser entries from committed metadata, `1292` records scanned, manual-entry/override/tombstone/path-alias/column-profile scaffolds, optional PySide6 GUI launch, source-browser CLI validation, Stage 5DP preservation, no target selected, no puzzle execution, no OCR/image forensics, no byte-stream generation, no CUDA, and no solve claim.
- Stage 5DS: expanded Music / Ouroboros / self-reference / token-block static-context source-lock addendum complete with `29` ignored community-theory files inventoried, `11` music candidates, `17` Ouroboros/self-reference context records, `4` token-block static-context records, `62` Stage 5DS Source Browser entries, Stage 5DR/Stage 5DG/Stage 5BD/active-lineage preservation, no target selected, no active input, no byte streams, no execution, and no solve claim.
- Stage 5DT: Operator Console number-fact card and evidence-reviewability upgrade complete with `1387` Source Browser entries loaded, `20` extracted number-fact cards, `13` vague facts needing enrichment, `1383` zero-fact-not-reviewed entries, `7` planned 20-entry review batches, enrichment overlay schemas/loader, GUI fact-card rendering, table/filter improvements, Stage 5DS/Stage 5DG/Stage 5BD/active-lineage preservation, no fact backfill, no target selected, no active input, no byte streams, no execution, and no solve claim.
- Stage 5DU: community visual/red-heading/negative-space source-lock addendum complete with `6` ignored local thread folders represented, `234` files inventoried, `75` canonical LP page images crosslinked, `72` review-only candidate records, `12` number-fact cards/overlays created or enriched, `1490` Source Browser entries validated, Stage 5DT/Stage 5DG/Stage 5BD/active-lineage preservation, no community code execution, no OCR/image forensics, no route extraction, no target selected, no byte streams, no execution, and no solve claim.
- Stage 5DV: Operator Console Source Browser performance/path-canonicalization repair complete with `1510` Source Browser entries validated, `1509` committed records scanned, `0` spurious root image/document paths, `0` duplicate present+missing path pairs, source-root-relative path resolution active, ChatGPT context expanded, Stage 5DU/Stage 5DT/Stage 5DG/Stage 5BD/active-lineage preservation, no number-fact review batch, no source-lock rewrite, no target selected, no byte streams, no execution, and no solve claim.
- Stage 5DX: Source-lock number-fact review batch 002 complete with `20` selected records reviewed, `23` review-only NumberFactCard overlays, overlay-only fact-card support preserved, `1546` Source Browser entries validated, `1545` committed records scanned, `80` fact cards after overlays, `0` spurious root image/document paths, `0` duplicate present+missing path pairs, Stage 5DW/Stage 5DV/Stage 5DU/Stage 5DG/Stage 5BD/active-lineage preservation, no direct historical fact backfill, no source-lock rewrite, no target selected, no route extraction, no byte streams, no execution, and no solve claim.
- Stage 5DY: Validation performance and stage-isolation repair complete with `6` validation profiles, parallel worker cap `8`, full serial pytest default `false`, stage-isolation repair `true`, shared-schema collision guard `true`, non-mutating validator guard `true`, Stage 5DX preservation, Stage 5BD run-plan IDs `10`, active-lineage records `8`, no number-fact batch 3, no target selected, no byte streams, no execution, and no solve claim.
- Stage 5DZ: Triangle/Page32 bounded-findings source-lock addendum complete with `7` PDD153 triangle findings, `8` Page32 findings, `12` Source Browser overlays, PDD heading canonicalization warning, WAY-anchor arithmetic recorded as candidate-only, Page32 red-header `3299 -> 2472` context, direct-method negative-result notes, future design notes, no number-fact batch 3, no target selected, no route extraction, no route streams, no byte streams, no image forensics/OCR, no execution, and no solve claim.
- Stage 5EA: Validation throughput and historical-test isolation repair complete with `26` Stage 5EA records, `21` Stage 5EA schemas, current-stage registry routing, Stage 5DZ completion verification, Source Browser number-fact overlay caching, hyphenated stage-id wrapper repair, weighted pytest shard policy, orphan-process timeout policy, no number-fact batch 3, no source-lock evidence updates, no target selected, no active ingestion, no byte streams, no execution, and no solve claim.
- Stage 5EB: Validation finalization and 10-worker policy repair complete with `23` Stage 5EB records, `22` Stage 5EB schemas, Stage 5EA preservation, 10-worker local validation defaults/caps, full-serial-rare fallback policy, current-stage registry finalization handoff policy, generic stage wrapper repair, doc-tier policy, duration-aware pytest shard/rerun guidance, Source Browser cache reuse evidence, no number-fact batch 3, no source-lock evidence updates, no target selected, no active ingestion, no byte streams, no execution, and no solve claim.
- Stage 5ED: Source-lock number-fact review batch 004 complete with `20` reviewed entries, `25` review-only overlays, `142` Source Browser fact cards after overlay load, Stage 5EC overlays and Stage 5EB 10-worker validation policy preserved, zero Source Browser validation errors, no source-lock evidence updates, no historical source-lock rewrites, no target selected, no route extraction, no byte streams, no execution, and no solve claim.
- Stage 5EE: Source-lock number-fact review batch 005 complete with `20` reviewed entries, `25` review-only overlays, `167` Source Browser fact cards after overlay load, Stage 5ED overlays and Stage 5EB 10-worker validation policy preserved, zero Source Browser validation errors, no source-lock evidence updates, no historical source-lock rewrites, no target selected, no route extraction, no byte streams, no execution, and no solve claim.
- Stage 5EG: Post-edit doc-staleness guardians complete with the stale-current scanner, scanner-backed project hooks, read-only custom-agent configs, daily report-only automation setup, Source Browser loadability preservation, and zero strict stale-current errors.
- Stage 5EH: Lag5/outguess/byte-string/red-number/F5 context source-lock addendum complete with 5 Lag5 files inventoried, 8 lp_outguessed signed outputs, 23 future probe manifests, 36 review-only overlays, zero Source Browser errors, and no execution.
- Stage 5EI: Final Stage 5 triangle-transposition and diagnostics transition complete with 25 records, PDD153/T17 geometry, 22/24 triangular-transposition taxonomy ambiguity, no-plaintext route-fingerprint policy, 7 review-only overlays, Stage 5EH preservation, stale-current strict errors `0`, and Stage 6 readiness routing.
- Stage 6: Diagnostic backlog census, discovery-probe readiness, result-bundle policy, and Stage 7/8/9 handoff complete without execution.
- Stage 6B: Diagnostic-readiness repair and hook stabilization complete; Stage 6 mappings are repaired, the Stage 7 menu is partial/non-executable, and hooks default to report-only.
- Stage 6C: OUROBOROS/I31 circumference source-lock addendum complete with 9 historical-route records, 12 review-only overlays, 10 disabled future probes, Page32 3222 red/highlight status not source-confirmed, and Stage 6D routing.
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
- Latest operator-console/source-lock stage: Stage 5EE implements source-lock number-fact review batch 005 as reviewability overlay metadata. It validates `1724` Source Browser entries, adds `25` overlays for `20` selected source-register/music/Fandom/residual NumberFacts records, supports overlay-only fact cards, preserves Stage 5ED overlays, Stage 5EB's 10-worker validation policy, and Stage 5BD/active-lineage boundaries, and leaves Deep Research acceptance, combined-gate satisfaction, activation authorization, active input, dry-run ingestion, byte-stream generation, target-class validation, Tor access, route extraction, DWH/hash/preimage search, OCR/image forensics/AI interpretation, audio/stego/native/VM/CUDA/scoring/benchmark work, community-code execution, raw-source mutation, source-lock rewrite, direct historical fact backfill, and future token-block execution blocked.
- Stage 5EF: Latest current-truth/doc-policy stage inserts anti-drift infrastructure before number-fact review batch 006. It makes `data/project-state/current-stage-state.yaml` authoritative, classifies broad Markdown docs as mirrors or historical evidence, adds deterministic context-pack templates, report-only automation templates, inactive advisory-hook policy, skills deferral, and focused validators, and keeps all puzzle/source-lock/execution guardrails closed.
- Latest validation repair stage: Stage 5DY records the Stage 5DX slow-validation diagnostics and adds staged validation profiles. Stage 5DZ preserves those profiles while adding review-only Triangle/Page32 source-lock enrichment. Future local work should use focused or stage-fast checks during implementation, local-fast before commit, and full-parallel near final. Full serial pytest is a rare fallback, not the default per-stage loop.
- Latest validation stage: Stage 5AX adds opt-in parallel validation infrastructure with `10` parallel-safe commands, `6` serial commands, `1` blocked command, separated logs, failure aggregation, and safety audits while keeping git/GitHub/network/generated-output-writing operations serial. Stage 5DQ preserves the local parallel-validation and pytest cap at 8 workers for Stage 5CM and later.
- Latest doc-staleness stage: Stage 5AH repairs README stage-ledger coverage, operational-file-map coverage, and current/next-stage consistency checks before curated extraction. Stage 5EE updates current/next-stage records to Stage 5EE complete and Stage 5EF next.
- Latest validation infrastructure stage: Stage 5EB finalizes the 10-worker local validation policy, full-serial-rare fallback boundary, current-stage registry finalization handoff policy, generic stage wrapper aliases, pytest shard/rerun guidance, and Source Browser overlay-cache reuse evidence.
- Historical next after Stage 5EH: Stage 5EI - Source-lock number-fact review batch 006, without execution.

## How To Use This Repo

1. Set up Python 3.12 and a local virtual environment using the [Windows](tutorials/02-windows-setup.md) or [Linux](tutorials/03-linux-setup.md) tutorial.
2. Run the local validation stack before trusting a change:

```powershell
.\.venv\Scripts\python.exe -m ruff check python/libreprimus tests/python
.\scripts\ci\run-stage-validation.ps1 -Stage stage5ed -Profile full-parallel -Workers 10 -PytestWorkers 10
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

<!-- BEGIN stage5ef -->
## Stage 5EF Current Status

The current authoritative stage registry is `data/project-state/current-stage-state.yaml`.

Latest completed: Stage 5EF - Plan-mode current-truth ledger and drift-audit foundation.

Next routed: Stage 5EG - Source-lock number-fact review batch 006, without execution.

Stage 5EF is an anti-drift/current-truth foundation inserted before number-fact review batch 006. Batch 006 is
deferred to Stage 5EG.
<!-- END stage5ef -->

<!-- BEGIN stage5eg -->
## Stage 5EG Current Status

The authoritative current-stage registry is `data/project-state/current-stage-state.yaml`.

Latest completed: Stage 5EG - Post-edit doc-staleness guardians, read-only auditor agents, stop-hook drift gate, and daily automation setup, without puzzle execution.

Next routed: Stage 5EH - Lag5 phenomenon source-lock, diagnostic/probe manifest, and enriched fact cards, without execution.
<!-- END stage5eg -->

<!-- BEGIN stage5eh -->
## Stage 5EH Current Status

The authoritative current-stage registry is `data/project-state/current-stage-state.yaml`.

Latest completed: Stage 5EH - Lag5/outguess/byte-string/red-number/F5 context source-lock addendum, diagnostic probe manifests, and enriched fact cards, without execution.

Next routed: Stage 5EI - Source-lock number-fact review batch 006, without execution.
<!-- END stage5eh -->

<!-- stage6:start -->
## Stage 6 Readiness Snapshot

Stage 6 is complete as metadata-only diagnostic readiness. The project now has a bounded source-root census, diagnostic-backlog census, future discovery-probe registry, bridge/keeper taxonomies, no-lossy Stage 7 archive policy, and Stage 8/9 triangle boundaries. The next routed stage is Stage 6B, not execution.
<!-- stage6:end -->

<!-- stage6b:start -->
## Stage 6B Current State

Stage 6B is complete as deterministic repair metadata. It fixes Stage 6 probe-family/source/readiness planning records, marks the Stage 7 menu as partial and non-executable, and stabilizes project-local hooks as report-only by default. At the time of Stage 6B closeout, Stage 6C remained the next planning stage for OUROBOROS/I31 source-lock addendum work.
<!-- stage6b:end -->

<!-- stage6c:start -->
## Historical Stage 6C Current-Status Mirror

At the time of Stage 6C, Stage 6C - OUROBOROS / I=31 circumference / Page32 spiral geometry source-lock addendum, without execution was the latest completed stage.

Historical next prompt at Stage 6C closeout: Stage 6D - Final finite Stage 7 probe manifest and archive-run contract, without execution. The OUROBOROS/I31 bridge is review-only metadata: OUROBOROS=167, the vowel/voice layer is 31=GP(I), and Page32 3222 remains source-backed only as a grid/spiral value unless separately source-confirmed as highlighted.
<!-- stage6c:end -->

<!-- stage6d:start -->
## Historical Stage 6D Current Status

Historical prior-stage note: Stage 6F was the latest completed stage when this old section was written.

Historical next prompt from that older section: Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution. Stage 6D records the 86/89 doublet counts as boundary-policy-specific metadata, not solve evidence or execution authorization.
<!-- stage6d:end -->

<!-- stage6e:start -->
## Historical Stage 6E Boundary

Historical prior-stage note: Stage 6F was the latest completed stage when this old section was written.

Historical routed stage from that older section: Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution.

Stage 6E classified all stale-current warning-domain findings into named buckets, installed bounded report-only preprompt doc-staleness advisory behavior, source-locked finite bridge facts, superseded the stale Stage 6B Stage 6C token-block projection precondition, and built Stage 6F source-root/probe traceability inputs.

Stage 6E did not create a final Stage 7 manifest, finalize an archive-run contract, create a result archive, run probes, generate route or byte streams, run OCR/image/stego/CUDA/scoring/benchmarks, select targets, or make a solve claim.
<!-- stage6e:end -->

<!-- stage6f:start -->
## Historical Stage 6F Boundary

Historical prior-stage note: Stage 6F was the latest completed stage when this old section was written.

Historical routed stage from that older section: Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution.

Stage 6F repaired malformed/stale current mirrors, added file-content validators for high-risk docs, preserved Stage 6E source-lock payloads through a supersession layer, added preflight self-report exclusion, verified report-only hook behavior where local launcher tests can support it, recorded the Ciada/Cicada source-root alias policy, crosslinked the dju-bei backlog gap, and installed strict Codex acceptance criteria.

Stage 6F did not create a final Stage 7 manifest, finalize an archive-run contract, create result archives, run probes, add new theory records, add overlays, generate route or byte streams, run OCR/image/stego/CUDA/scoring/benchmarks, select targets, or make a solve claim.
<!-- stage6f:end -->

<!-- stage6g:start -->
## Historical Stage 6G Boundary

Historical latest stage at Stage 6G closeout: Stage 6G - Current-doc acceptance repair, Stage 6H source-lock handoff repair, hook confirmation, and acceptance-policy hardening, without execution.

Historical Stage 6G route pointed to Stage 6H - Dot-angle and right-triangle number-triangle bridge source-lock addendum, without execution. Stage 6H is source-lock/readiness addendum work, not final Stage 7 manifest construction, because recent dot-angle/right-triangle number-triangle material remains chat-only pending source-lock.

Stage 6G repaired current-doc and handoff integrity, expanded acceptance-policy integration, verified hooks where local direct/script launcher tests can support it, and recorded honest operator-confirmation risk for actual Codex runner semantics. It did not source-lock the new dot/triangle material, create probes or overlays, create a Stage 7 manifest or archive, generate route or byte streams, execute tools, select targets, or claim a solve.
<!-- stage6g:end -->
