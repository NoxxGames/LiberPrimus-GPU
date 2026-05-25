> This Wiki page mirrors $sourceRel. The repository tutorial file is the source of truth.

# Codex Assisted Development

## Purpose

Use Codex safely for scoped repository stages.

## Prompt Checklist

- State the current stage and latest commit.
- Include explicit non-goals.
- List raw/generated files that must not be staged.
- Require tests, docs, developer logs, commit, push, and CI verification.
- Require GitHub issue updates when relevant.
- For Discord stages, state that raw logs, generated shards, message bodies, usernames, user IDs, message IDs, and private URLs must not be staged.
- For post-Discord manifests, state whether the stage is queue-only or execution-authorized.
- For Stage 3S/3T/3U-style execution, state the exact manifest ID, candidate or claim cap, generated output paths, and that no other post-Discord manifest may run in the same stage.
- For Stage 3V-style stego work, state whether missing OutGuess tools/assets should skip, list the exact manifest, and prohibit broad image scans.
- For Stage 3W-style consolidation, state that no experiments should run and require source-of-truth docs plus anti-drift checks to stay synchronized.
- For Stage 3X-style CLI modularisation, state that command names, options, help behavior, output shape, and exit semantics must be preserved and that command-surface tests must be added or updated.
- For Stage 3Y-style research synthesis, require `docs/roadmap/staged-plan.md`, `data/research/` ledgers, anti-drift checks, and `libreprimus research-synthesis validate`. Do not execute experiments.
- For Stage 3Z-style onboarding work, require `docs/onboarding/` maps, staged-plan updates, direction-change records if the roadmap changes, and state-drift tests. Do not execute experiments.
- For Stage 4A-style Deep Research handoff work, require `redacted_public` output, ignored static-site/bundle paths, aggregate-only committed records, no raw Discord logs, no usernames/IDs/private URLs, and no copied LP page images in Git.
- For Stage 4A follow-up static-site work, require noindex metadata, `robots.txt`, privacy notice, SFTP checklist, deterministic site manifest, and validation that generated site files remain ignored.
- For Stage 4B-style source-lock triage, require allowlisted public-source promotion, unsafe/private link rejection, review-only visual observations, negative-control records, disabled manifests, and no experiment execution.
- For Stage 4C-style visual annotation work, require schemas, task records, generated ignored annotation-site support, no coordinate invention, no meaning inference, no OCR/AI/ML, no experiment execution, and `usable_as_experiment_seed=false`.
- For Stage 4D-style bounded numeric verifier work, require no-fudge policy, exact source-backed claims only, fixed route spaces, generated ignored outputs, skipped/deferred records when evidence is missing, no cookie/cuneiform execution unless explicitly scoped, no CUDA, and no solve claim.
- For Stage 4E-style source-delta work, require explicit remote target, metadata-only tree/path records, ignored local cache, no blind mirror, no raw image/audio/font/archive commits, disabled future manifests only, no image/stego processing, and no solve claim.
- For Stage 4F-style stego/audio fixture source-locking, require fixture metadata only, source-health records, toolchain requirement records, disabled future manifests, no raw artefact commits, no OutGuess/OpenPuff/MP3Stego/hexdump/audio execution, and no solve claim.
- For Stage 4G-style cookie refresh work, require source-backed exact strings only, manifest-declared variants and algorithms, exact digest comparison, generated ignored outputs, method-ledger updates on zero matches, no fuzzy/partial matching, no hashcat, no GPU/CUDA, and no solve claim.
- For Stage 4H-style CPU batch API work, require normalized token streams, explicit transform candidates, deterministic output hashes, synthetic tests, stable CLI behavior, generated ignored outputs, no new transform semantics without docs/tests, no CUDA, and no solve claim.
- For Stage 4I-style scoring consolidation work, require scorer records, finite confidence labels, compatibility mapping, calibration notes, CPU batch compatibility checks, generated ignored outputs, no new scorer invention, no CUDA, and no solve claim.
- For Stage 4J-style observation review work, require review-state schemas, decisions, promotion gates, quarantine records, path sanitisation checks, stale-doc repair, generated ignored outputs, no experiment execution, and no solve claim.
- For Stage 4K-style source-lock snapshot work, require allowlisted public sources only, explicit `--allow-network` for fetches, GitHub commit-addressed references where possible, ignored local cache, copyright notes, generated ignored reports, no broad crawl or mirror, no raw artefact commits, and no solve claim.
- For Stage 4L-style promotion-ledger work, require explicit review-decision and source-lock references, blocker records for non-ready observations, `execution_enabled=false`, no manifest execution, no raw/generated commits, and no solve claim.
- For Stage 4M-style image preflight work, require metric-only image metadata/compression records, source-variant blocked status when external bytes are absent, review-only artefact candidates, bigram/Fibonacci readiness blocked pending matrix/null controls, generated ignored outputs, no OCR/AI/ML/stego, and no solve claim.
- For Stage 4N-style stego/audio positive-control work, require fixture-readiness records, cache policy, expected-output metadata, toolchain readiness, synthetic controls, generated ignored outputs, no historical stego/audio tool execution, no raw artefact commits, and no solve claim.
- For Stage 4O-style CPU batch adapter work, require solved-fixture-safe streams, adapter coverage records, parity expectation hashes, scoring compatibility checks, generated ignored outputs, unchanged transform semantics, no solved-baseline expectation changes, no CUDA, and no solve claim.
- For Stage 4P-style result-store unification work, require source inventory records, Stage 4I-compatible score-summary views, method-status joins, cross-stage reports, generated ignored outputs, no raw-data reads, no scorer invention, no experiment execution, no SQLite staging, no CUDA, and no solve claim.
- For Stage 5A-style CUDA planning work, require target plans, non-target records, parity scaffolds, implementation gates, generated ignored outputs, no CUDA source changes, no GPU benchmarks, no speedup claims, no raw-data reads, and no solve claim.
- For Stage 5B-style CUDA parity harness work, require harness plans, parity fixtures, backend capability profiles, future-kernel matrix rows, generated ignored outputs, no CUDA source changes, no GPU benchmarks, no required local 16GB profile, no speedup claims, no raw-data reads, and no solve claim.
- For Stage 5C-style CUDA build/device work, require no-GPU-safe build profiles, toolchain records, device records, optional smoke-build records, generated ignored outputs, no CUDA source changes, no GPU benchmarks, no required local 16GB profile, no speedup claims, no website expansion, no raw-data reads, and no solve claim.
- For Stage 5D-style native CPU backend work, require C++ CPU-only backend tests, deterministic threading parity, native/Python parity, generated ignored outputs, no CUDA source changes, no GPU benchmarks, no speedup claims, no C++ Python worker launches, no website expansion, no raw-data reads, and no solve claim.
- For Stage 5E-style CUDA kernel contract work, require selected-contract records, native parity adapter mapping, implementation-readiness records, generated ignored outputs, no CUDA source changes, no GPU benchmarks, no speedup claims, no website expansion, no raw-data reads, and no solve claim.
- For Stage 5F-style synthetic CUDA kernel work, require the selected `shift_score_kernel` contract, Stage 5D native hash, synthetic-only records, no-GPU-safe validation, no real Liber Primus CUDA data, no GPU benchmarks, no speedup claims, no website expansion, no raw-data reads, and no solve claim.
- For Stage 5G-style CUDA parity reporting work, require Stage 5F synthetic parity records, conservative CUDA-C `.cu`/`.cuh` subset checks, solved-fixture-safe blockers, no-GPU-safe validation, no new kernels, no real Liber Primus CUDA data, no GPU benchmarks, no speedup claims, no website expansion, no raw-data reads, and no solve claim.
- For Stage 5K-style Gematria CUDA parity reporting work, require Stage 5J synthetic Gematria parity records, Stage 5H native fixture hash references, device-code subset audit records, solved-fixture-safe blockers, score-summary preflight records, no-GPU-safe validation, no new kernels, no CUDA source changes, no CUDA execution, no real Liber Primus CUDA data, no solved or unsolved page CUDA use, no GPU benchmarks, no speedup claims, no website expansion, no raw-data reads, and no solve claim.
- For Stage 5L-style solved-fixture Gematria token-mapping work, require Stage 5K preflight records, Stage 4O solved-fixture-safe stream references, exact `0..28` token buffers, token-kind and separator preservation, native output-token hash records, score-summary shape records, no-GPU-safe validation, no new kernels, no CUDA source changes, no CUDA execution, no real Liber Primus CUDA data, no solved or unsolved page CUDA use, no GPU benchmarks, no speedup claims, no website expansion, no raw-data reads, and no solve claim.
- For Stage 5M-style solved-fixture Gematria CUDA parity work, require Stage 5L token mappings and native hashes, exactly five approved buffers, use of only the existing `gematria_mod29_shift_score_kernel`, no new kernels, no device arithmetic changes, host-runner-only CUDA source changes if needed, no unsolved-page CUDA, no real Liber Primus CUDA data, no GPU benchmarks, no speedup claims, no website expansion, generated reports ignored, and no solve claim.
- For Stage 5P-style CUDA result-store integration work, require Stage 5O repeat parity records, Stage 4P/Stage 4I-compatible compact metadata, generated-body publication blocks, method-status non-upgrade records, controlled expansion candidates, no CUDA execution, no CUDA source changes, no new kernels, no unsolved-page CUDA, no GPU benchmarks, no speedup claims, generated reports ignored, and no solve claim.
- For Stage 5Q-style expansion candidate mapping work, require Stage 5P controlled expansion records, exact Stage 5L/5M/5O duplicate exclusion, source-backed token mappings, native parity hashes, Stage 4P/Stage 4I-compatible preflight, no CUDA execution, no CUDA source changes, no new kernels, no unsolved-page CUDA, no GPU benchmarks, no speedup claims, generated reports ignored, and no solve claim.
- For Stage 5Z-style prime-minus-one CUDA contract work, require Stage 5Y compact reporting/readiness records, CUDA contract records, CUDA-C style kernel ABI records, host-runner and buffer contracts, validation vectors, future parity plans, result-store compatibility records, full-p56 blocker preservation, scored-experiment deferral, implementation-readiness gates, generated reports ignored, no native execution, no CUDA execution, no CUDA source changes, no new kernels, no p56/full-p56 CUDA, no unsolved-page CUDA, no GPU benchmarks, no speedup claims, no generated-body publication, and no solve claim.
- For Stage 5AA-style prime-minus-one CUDA synthetic parity work, require the Stage 5Z synthetic validation vector, a synthetic-only CUDA kernel entrypoint, host-computed hash comparison against the Stage 5Z expected hash, device-code subset audit records, p56/full-p56 blockers, scored-experiment deferrals, generated ignored reports, `codex-output/**` ignored, no p56/full-p56 CUDA, no unsolved-page CUDA, no real Liber Primus CUDA data, no benchmarks, no speedup claims, no website expansion, no method-status upgrade, and no solve claim.
- For Stage 5AC-style prime-minus-one CUDA synthetic reporting work, require Stage 5AA synthetic parity records, Stage 5AB doc-staleness records, compact result-store/score-summary integration, method-status non-upgrade records, generated-body policy, bounded-p56 preflight, full-p56 blocker preservation, scored-experiment deferrals, generated ignored reports, `codex-output/**` ignored, no CUDA execution, no p56/full-p56 CUDA execution, no native execution, no CUDA source changes, no new kernels, no benchmarks, no generated-body publication, no method-status upgrade, and no solve claim.
- For Stage 5AD-style bounded p56 CUDA parity work, require the exact Stage 5Z bounded validation vector, Stage 5AC preflight records, Stage 5X expected hash, host-computed CUDA output hash, mismatch/pass/skip next-stage decision records, generated ignored reports, `codex-output/**` ignored, no full p56, no unsolved pages, no new kernels, no CUDA-facing source changes, no device arithmetic changes, no benchmarks, no scored experiments, no generated-body publication, no method-status upgrade, and no solve claim.
- For Stage 5AD-fix-style bounded p56 mismatch work, require committed Stage 5AD/5X/5W/5L source records, hash-lineage records, token/stream/formula traces, hash-material and reference-contract records, root-cause records, repair-readiness records, guardrails, generated ignored reports, `codex-output/**` ignored, no CUDA execution, no full p56, no unsolved pages, no new kernels, no CUDA-facing source changes, no benchmarks, no scored experiments, no generated-body publication, no method-status upgrade, and no solve claim.
- For Stage 5AE-style corrected bounded p56 reporting work, require Stage 5AD-fix source records, corrected formula-parity metadata, Stage 5AD historical-failure preservation, reference-contract and hash-material policy repair, result-store/score-summary integration, method-status non-upgrade records, generated-body policy, full-p56 and scored-experiment deferrals, archive/source-lock deferral records, generated ignored reports, `codex-output/**` ignored, no CUDA execution, no Stage 5AD reclassification as passed, no full p56, no unsolved pages, no new kernels, no CUDA-facing source changes, no benchmarks, no raw/archive processing, no generated-body publication, and no solve claim.
- For Stage 5AF/5AG-style source-harvester work, require source-manifest or local-inventory records, source-lock candidate/gap records, research-bundle readiness, local-only tool policy, generated ignored reports, `codex-output/**` ignored, no Google Drive storage, no live broad scraping, no raw download/source commits, no raw archive content commits, no CUDA execution, no CUDA source changes, no new kernels, no benchmarks, no scored experiments, no website expansion, and no solve claim.
- For Stage 5AI-style curated research-bundle work, require Stage 5AG inventory inputs, source-card and content-index metadata, website-ingest and Deep-Research pack records, missing-source plans, guardrails, generated ignored `research-inputs/stage5ai/` bodies, generated ignored `experiments/results/research-bundles/stage5ai/` reports, `codex-output/**` ignored, no Deep Research execution, no network fetch, no online clone, no Google Drive storage, no raw source commits, no website expansion, no hypothesis execution, no CUDA, no benchmarks, no scored experiments, and no solve claim.
- For Stage 5AJ-style UsefulFilesAndIdeas work, require ignored local `third_party/UsefulFilesAndIdeas/` inputs, compact workbook/link/source-card/content-index summaries, extraction-fidelity policy, redaction policy, scraper-capture profiles, Deep-Research readiness records, generated ignored `research-inputs/stage5aj/` bodies, generated ignored `experiments/results/source-harvester-usefulfiles/stage5aj/` reports, `codex-output/**` ignored, no live scraping, no network fetch, no online clone, no Google Drive storage, no raw workbook/image/text commits, no Deep Research execution, no website expansion, no hypothesis execution, no CUDA, no benchmarks, no scored experiments, and no solve claim.
- For Stage 5AK-style community-facts work, require ignored local `third_party/UsefulFilesAndIdeas/community-facts/` inputs, ordered attachment metadata, community claim records, correction logs, arithmetic-preflight metadata, private Deep-Research pack addenda, generated ignored `research-inputs/stage5ak/` bodies, generated ignored `experiments/results/source-harvester-community-facts/stage5ak/` reports, `codex-output/**` ignored, no live scraping, no Deep Research execution, no website expansion, no hypothesis execution, no OCR/AI/ML/image forensics, no CUDA, no benchmarks, no scored experiments, and no solve claim.
- For Stage 5AL-style website-ingest work, require committed metadata-only `data/website-ingest/stage5al/` records, publication gates, a private Deep Research export manifest, ignored `research-inputs/stage5al/` helper files, ignored `experiments/results/website-ingest/stage5al/` reports, public website-ready `0`, `codex-output/**` ignored, no raw/private body publication, no Deep Research execution, no public website publication, no live scraping, no Google Drive storage, no OCR/AI/ML/image/stego/audio tooling, no CUDA, no benchmarks, no scored experiments, and no solve claim.
- For Stage 5AM-style static website rendering, require committed `data/website-render/stage5am-*` metadata records, ignored `website-export/stage5am/` static site and ZIP outputs, ignored `experiments/results/website-render/stage5am/` reports, public website-ready `0`, preserved publication gates, no raw/private body publication, no Deep Research execution, no public website publication, no live scraping, no Google Drive storage, no OCR/AI/ML/image/stego/audio tooling, no CUDA, no benchmarks, no scored experiments, and no solve claim.
- For Stage 5AP-style token-block source-lock work, require committed `data/token-block/stage5ap-*`, `data/stego/stage5ap-outguess-*`, and `data/project-state/stage5ap-*` metadata records, canonical 32x8 transcription, logical coordinates, primary-60 mapping preflight, null controls, DWH context, OutGuess guardrails, generated ignored `experiments/results/token-block/stage5ap/` and `experiments/results/stego-controls/stage5ap/` reports, no raw image commits, no Deep Research execution, no OCR/AI/ML, no broad image forensics, no LP-page OutGuess, no hash/preimage search, no CUDA, no benchmarks, no scored experiments, no page-boundary finalisation, and no solve claim.
- For Stage 5AR-style coordinate-lock work, require committed `data/token-block/stage5ar-*` and `data/project-state/stage5ar-*` metadata records, selected original page-image hashes, source-backed page-split records, 256 pixel-coordinate records, case-ambiguity policy, coordinate validation, generated ignored `experiments/results/token-block/stage5ar/` reports, no screenshots/crops/modified images as coordinate truth, no raw image commits, no Deep Research execution, no OCR/AI/ML, no semantic image interpretation, no hidden-content image forensics, no stego execution, no hash/preimage search, no decode attempt, no CUDA, no benchmarks, no scored experiments, no page-boundary finalisation, and no solve claim.
- For Stage 5R-style expanded solved-fixture CUDA parity work, require Stage 5Q mapped candidates only, exclude Stage 5L/5M/5O consumed controls, keep blocked original-family fixtures blocked, use only the existing `gematria_mod29_shift_score_kernel`, no new kernels, no device arithmetic changes, no unsolved-page CUDA, no real Liber Primus CUDA data, no GPU benchmarks, no speedup claims, generated reports ignored, and no solve claim.
- For Stage 5S-style expanded CUDA result-store integration work, require Stage 5R committed parity records, compact Stage 4P/Stage 4I-compatible metadata only, generated-body publication blocks, method-status non-upgrade records, boundary review, controlled next-step decision, no CUDA execution, no CUDA source changes, no new kernels, no unsolved-page CUDA, no GPU benchmarks, no speedup claims, generated reports ignored, `codex-output/**` ignored, and no solve claim.
- For Stage 5V-style native Candidate Batch ABI conformance work, require Stage 5U ABI records, native adapter records, conformance fixtures, token-buffer/schedule/score-vector/top-k conformance, result-store conformance, implementation-status records, generated ignored outputs, `codex-output/**` ignored, no CUDA execution, no CUDA source changes, no native/CUDA CMake, no new kernels, no unsolved-page CUDA, no GPU benchmarks, no speedup claims, no raw-data reads, and no solve claim.
- For Stage 5W-style prime-minus-one native contract work, require Stage 5V conformance records, Stage 5U stream contracts, committed p56 solved-fixture-safe records, source inventory, source-backed stream formula/direction, deterministic schedules, Candidate Batch ABI mapping, native parity preparation, result-store preflight, guardrails, generated ignored outputs, `codex-output/**` ignored, no CUDA execution, no CUDA source changes, no native/CUDA CMake, no new kernels, no unsolved-page CUDA, no GPU benchmarks, no speedup claims, no invented p56 tokens, no raw-data reads, and no solve claim.
- For Stage 5X-style prime-minus-one no-GPU native parity work, require Stage 5W ready mappings only, execute only the synthetic prime control and bounded p56 mapping through the Python/native reference path, keep the full p56 mapping blocked, compare output hashes against Stage 5W expectations, write result-store and score-summary preflight records, keep generated reports and `codex-output/**` ignored, and do not run CUDA, modify CUDA source, run native/CUDA CMake, add kernels, run benchmarks, report speedups, publish generated bodies, process raw data, or make solve claims.
- For Stage 5Y-style prime-minus-one native reporting work, require committed Stage 5X parity records, compact parity-report/result-store/score-summary integration, method-status non-upgrade records, generated-body policy, full-p56 blocker preservation, CUDA contract readiness gating, bounded scored-experiment readiness records, generated ignored reports, `codex-output/**` ignored, no native parity execution, no CUDA execution, no CUDA source changes, no native/CUDA CMake, no new kernels, no full-p56 execution, no benchmarks, no speedup claims, no generated-body publication, no raw-data reads, and no solve claim.

## Commands

```powershell
git status --short
.\.venv\Scripts\python.exe -m pytest -q tests/python
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-state-drift
.\.venv\Scripts\python.exe -m libreprimus.cli research-synthesis validate --data-dir data/research --staged-plan docs/roadmap/staged-plan.md
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-all --allow-warnings
```

## What Not To Commit

Raw corpus material, generated outputs, root research reports, `.venv/`, build dirs, and wiki
worktrees. For Stage 3R/3S/3T/3U/3V-style work, also keep generated Discord review bundles, topic shards, promotion audit JSONL, post-Discord candidate JSONL, verification JSONL, hash candidate JSONL, OutGuess extraction JSONL, extracted payloads, summary JSON, and root report copies out of staging unless copied into `docs/` intentionally.

Keep `deep-research-reports/**` out of staging; it is local review material only.

For Stage 5AF and later source-harvester work, keep raw outputs under ignored local roots such as `third_party/`, `source-harvester-output/`, `harvest-output/`, or `research-inputs/`. Google/Dropbox/Colab sources require manual export to local ignored storage; do not use Google Drive as a project storage location. Stage 5AG local inventory records are metadata only; archive listings are not source truth. Stage 5AI generated bundle bodies are private/local handoff inputs under `research-inputs/stage5ai/`, Stage 5AJ UsefulFiles generated bodies are private/local handoff inputs under `research-inputs/stage5aj/`, Stage 5AK community-facts generated bodies are private/local handoff inputs under `research-inputs/stage5ak/`, Stage 5AL private Deep Research export helpers are private/local handoff inputs under `research-inputs/stage5al/`, and Stage 5AM static index files are private/local generated outputs under `website-export/stage5am/`; none is a committed source or publication artefact.

For Stage 4A and later Deep Research handoff work, use generated redacted bundles and aggregate
summaries instead of raw Discord logs. Generated static review sites, copied images, thumbnails,
shards, and upload archives remain ignored outputs.

If GitHub Wiki publishing fails, record the exact error and manual fix in
`docs/github/wiki-publish-report.md`; do not treat an unavailable Wiki remote as a reason to weaken
the repository tutorial source or validation scripts.

## Troubleshooting

If Codex sees unrelated untracked files, keep them out of staging unless the user explicitly asks
to include them.

If Codex creates disabled experiment manifests, verify `execution_enabled=false`,
`cuda_enabled=false`, `no_solve_claim=true`, `canonical_corpus_active=false`, and
`page_boundaries_final=false` before committing.

If Codex executes a bounded manifest, verify the command ran only the requested manifest, raw
Discord logs and raw page images were not processed, and generated result files remain ignored.

If Codex runs OutGuess regression, verify missing tools/assets are recorded as skips when allowed,
raw historical artefacts remain ignored, and non-empty payloads are not interpreted without expected
hash validation.

If Codex updates stage state, verify `STATUS.md`, `ROADMAP.md`, `AGENTS.md`, and `README.md` are
synchronized with `docs/roadmap/staged-plan.md` and relevant `docs/onboarding/` maps, then run
`libreprimus consistency check-state-drift` before staging.

If Codex retires, reopens, or reprioritises a method family, update `data/research/` ledgers and run
`libreprimus research-synthesis validate` before staging.

If Codex promotes public sources or visual observations, verify `libreprimus source-lock-triage validate`
and keep generated triage diagnostics under ignored `experiments/results/source-lock-triage/`.

If Codex creates visual annotation tasks, verify `libreprimus visual-annotation validate`, keep
generated annotation sites/templates under ignored `experiments/results/visual-annotation/`, and
do not mark visual observations as verified or usable as experiment seeds.

If Codex runs bounded numeric verification, verify `libreprimus bounded-numeric validate`, keep
generated JSON/JSONL outputs under ignored `experiments/results/bounded-numeric/`, and reject
nearest-prime, arbitrary +/-n, post-hoc row/column arithmetic, fuzzy matching, route expansion,
cookie pack execution, and cuneiform seed execution unless an explicit future stage scopes them.

If Codex source-locks stego/audio fixtures, verify `libreprimus stego-fixtures validate`, keep
generated fixture diagnostics under ignored `experiments/results/stego-fixtures/`, and do not run
OutGuess, OpenPuff, MP3Stego, hexdump/strings, or audio rendering in that stage.

If Codex runs a source-delta audit, verify `libreprimus source-delta-audit validate`, keep generated
JSON/JSONL outputs under ignored `experiments/results/source-delta/`, keep raw cache contents under
ignored `third_party/CicadaSolversIddqd/`, and commit metadata records only.

If Codex runs a cookie refresh, verify `libreprimus cookie-refresh validate`, keep generated
candidate/exact-match/duplicate/warning/summary JSON under ignored `experiments/results/cookie-refresh/`,
and do not add arbitrary strings after seeing zero matches.

If Codex changes the CPU batch API, verify `libreprimus cpu-batch validate-manifest`,
`libreprimus cpu-batch validate-results`, adapter coverage, synthetic output hash tests, and
the CPU/CUDA parity contract before staging. Do not add GPU code as part of CPU batch API work.

If Codex changes scoring behavior, verify `libreprimus scoring validate`,
`libreprimus scoring check-cpu-batch-compatibility`, confidence-label mapping tests, and
calibration notes before staging. Score labels are triage metadata only and must not imply solved
or plaintext verified.

If Codex changes result-store unification behavior, verify `libreprimus result-store validate-stage4p`,
keep generated unified JSON/JSONL/SQLite files under ignored `experiments/results/result-store-unification/`,
preserve Stage 4I labels, and do not invent scorer semantics or reinterpret old noisy results.

If Codex changes Stage 5R expanded Gematria CUDA parity behavior, verify
`libreprimus gematria-expanded-solved-fixture-cuda validate-stage5r`, keep generated reports under
ignored `experiments/results/gematria-expanded-solved-fixture-cuda/stage5r/`, keep `codex-output/**`
ignored, and do not add kernels, benchmarks, speedup claims, generated-body publication, or
unsolved-page CUDA.

If Codex changes Stage 5T CUDA solved-family readiness behavior, verify
`libreprimus cuda-solved-family-readiness validate-stage5t`, keep generated reports under ignored
`experiments/results/cuda-solved-family-readiness/stage5t/`, keep `codex-output/**` ignored, and do
not run CUDA, modify CUDA source, add kernels, run benchmarks, publish generated bodies, or treat
shift-score parity as original transform-family CUDA verification.

If Codex changes Stage 5V native Candidate Batch ABI conformance behavior, verify
`libreprimus native-candidate-batch-conformance validate-stage5v`, keep generated reports under
ignored `experiments/results/cuda-candidate-batch-abi-conformance/stage5v/`, keep
`codex-output/**` ignored, and do not run CUDA, modify CUDA source, run native/CUDA CMake, add
kernels, run benchmarks, publish generated bodies, or treat shape-only records as implemented
family semantics.

If Codex changes Stage 5W prime-minus-one native contract behavior, verify
`libreprimus prime-minus-one-native-contract validate-stage5w`, keep generated reports under ignored
`experiments/results/prime-minus-one-native-contract/stage5w/`, keep `codex-output/**` ignored, and
do not run CUDA, modify CUDA source, run native/CUDA CMake, add kernels, run benchmarks, publish
generated bodies, invent p56 token buffers, or treat p56 readiness as a solve claim.

If Codex changes Stage 5X prime-minus-one no-GPU native parity behavior, verify
`libreprimus prime-minus-one-native-parity validate-stage5x`, keep generated reports under ignored
`experiments/results/prime-minus-one-native-parity/stage5x/`, keep `codex-output/**` ignored, and
do not run CUDA, modify CUDA source, run native/CUDA CMake, add kernels, run benchmarks, publish
generated bodies, execute the blocked full p56 mapping, or treat parity hashes as solve evidence.

If Codex changes Stage 5Y prime-minus-one native reporting behavior, verify
`libreprimus prime-minus-one-native-reporting validate-stage5y`, keep generated reports under
ignored `experiments/results/prime-minus-one-native-reporting/stage5y/`, keep `codex-output/**`
ignored, and do not rerun native parity, run CUDA, modify CUDA source, run native/CUDA CMake, add
kernels, run benchmarks, publish generated bodies, execute the blocked full p56 mapping, upgrade a
method family to solved, or treat reporting records as solve evidence.

If Codex changes observation review behavior, verify `libreprimus observation-review validate`,
`libreprimus observation-review check-paths`, promotion-gate tests, quarantine tests, and path
sanitisation tests before staging. Review-only observations cannot become experiment seeds.

If Codex source-locks public snapshots, verify `libreprimus source-lock-snapshots validate`, keep
generated reports under ignored `experiments/results/source-lock-snapshots/`, keep cache contents
under ignored `third_party/SourceSnapshots/`, and do not commit binaries, images, audio, fonts,
archives, raw Discord material, raw page images, or broad repository mirrors.

If Codex changes CLI registration, verify `python -m libreprimus.cli --help`, selected group
`--help` commands, and the Stage 3X command-surface tests before staging. Do not create
`python/libreprimus/cli/` while `python/libreprimus/cli.py` remains the public entrypoint.

If Codex changes Stage 5AN private Deep Research export behavior, verify
`libreprimus deep-research-export validate-stage5an`, keep generated content packs under ignored
`deep-research-content-packs/stage5an/`, keep hosted private content and combined webroots under
ignored `website-export/stage5an/`, keep `codex-output/**` ignored, and do not stage ZIP archives,
generated private bodies, hosted HTML/JSON files, raw `third_party/**`, raw workbooks/images/PDFs,
or local absolute/private identifiers. Copy the contents of `website-export/stage5an/webserver-root/`
to the private webserver root only after validation and access-control review.
# Stage 4Q Codex Output Boundary

Stage 4Q writes a local completion handoff under `codex-output/`. That directory is ignored and must not be staged. The committed source of truth is the Stage 4Q code, schemas, manifests, docs, and aggregate records under `data/`.

When using Codex after Stage 5AD, cite the Stage 5AD bounded p56 CUDA run, parity, result-store preflight, score-summary preflight, full-p56 blocker, scored-experiment deferral, doc-staleness validation, device-subset audit, next-stage decision, and summary records; the Stage 5AC synthetic parity report, result-store integration, score-summary integration, method-status impact, generated-body policy, bounded-p56 preflight, full-p56 blocker, scored-experiment deferral, doc-staleness validation, next-stage decision, and summary records; the Stage 5AB document-staleness source-of-truth, operational file map, findings, summary, and consistency-check records; the Stage 5AA synthetic CUDA kernel implementation, run, parity, device-subset audit, result-store preflight, p56/full-p56 blocker, scored-experiment deferral, next-stage decision, and summary records; the Stage 5Z CUDA contract, host-runner, buffer, validation-vector, future parity plan, result-store compatibility, full-p56 blocker, scored-experiment deferral, implementation-readiness gate, next-stage decision, and summary records; the Stage 5Y parity-report, result-store integration, score-summary integration, method-status impact, generated-body policy, full-p56 blocker preservation, CUDA contract readiness-gate, bounded scored-experiment readiness, guardrail, next-stage decision, and summary records; the Stage 5X native run, native parity, result-store preflight, score-summary preflight, full-p56 blocker, guardrail, next-stage decision, and summary records; the Stage 5W prime-minus-one source inventory, stream contract, prime schedule, Candidate Batch ABI mapping, native parity preparation, result-store preflight, guardrail, next-stage decision, and summary records; the Stage 5V native adapter, conformance fixture, token-buffer, schedule, score-vector, top-k, result-store, implementation-status, next-stage decision, and summary records; and the Stage 5U Candidate Batch ABI, token-buffer, transform-parameter, key-schedule, stream-schedule, score-vector, top-k, backend-surface, result-store compatibility, ABI gap closure, and next-stage decision records. Also preserve the Stage 5T solved-family inventory/parity matrix/kernel-readiness/ABI-gap/benchmark-readiness/guardrail records, Stage 5S compact integration records, Stage 5R expanded parity records, Stage 5Q candidate mappings, Stage 5O repeat-run/repeat-parity/result-store/score-summary/expansion-decision records, Stage 5N parity-report/gate/boundary/preflight/guardrail records, Stage 5M run/parity/boundary records, Stage 5L token-mapping/native-parity records, Stage 5K Gematria parity-reporting/preflight records, Stage 5J Gematria CUDA kernel records, Stage 5I Gematria CUDA preparation records, Stage 5H Gematria mod-29 `shift_score` contract records, Stage 5G parity-reporting/device-code audit records, Stage 5F synthetic `shift_score_kernel` parity records, Stage 5E selected contract, Stage 4O CPU batch parity expectations, Stage 4P unified result surfaces, Stage 4Q benchmark plans, Stage 5A target-plan/scaffold/gate records, Stage 5B harness/backend/matrix records, Stage 5C build/device records, and Stage 5D native CPU backend/threading records. Do not let ABI, prime-stream contract, no-GPU native parity, synthetic CUDA parity metadata, doc-staleness repair records, bounded-p56 preflight records, or a bounded-p56 mismatch turn into full p56 CUDA, broad CUDA implementation, real Liber Primus CUDA execution, solved or unsolved page CUDA use, GPU benchmarking, scored experiments, generated result-body publication, website expansion, method-status upgrades, or `codex-output/**` staging without an explicit prompt.

Stage 5V completion handoffs belong under ignored `codex-output/stage5v-codex-completion.md`.
Stage 5W completion handoffs belong under ignored `codex-output/stage5w-codex-completion.md`.
Stage 5X completion handoffs belong under ignored `codex-output/stage5x-codex-completion.md`.
Stage 5Y completion handoffs belong under ignored `codex-output/stage5y-codex-completion.md`.
Stage 5AA completion handoffs belong under ignored `codex-output/stage5aa-codex-completion.md`.
Stage 5AB completion handoffs belong under ignored `codex-output/stage5ab-doc-staleness-codex-completion.md`.
Stage 5AH completion handoffs belong under ignored `codex-output/stage5ah-codex-completion.md`; Stage 5AH generated reports belong under ignored `experiments/results/doc-staleness/stage5ah/`.
Stage 5AI completion handoffs belong under ignored `codex-output/stage5ai-codex-completion.md`; Stage 5AI generated bundle reports belong under ignored `experiments/results/research-bundles/stage5ai/`.
Stage 5AJ completion handoffs belong under ignored `codex-output/stage5aj-codex-completion.md`; Stage 5AJ generated bundle/report bodies belong under ignored `research-inputs/stage5aj/`, `experiments/results/research-bundles/stage5aj/`, and `experiments/results/source-harvester-usefulfiles/stage5aj/`.

For Stage 5AH-style documentation repair, validate the active source of truth with `data/project-state/stage5ah-doc-staleness-source-of-truth.yaml`, run the stage-ledger, operational-file-map coverage, current/next-stage, and Stage 5AH validation commands, and keep Stage 5AI curated local extraction as the next bounded source-provenance step. For Stage 5AI/5AJ/5AK/5AL/5AM/5AN-style curation, rendering, and private content-pack export, validate the committed source-harvester, website-render, and deep-research-export records and keep Stage 5AO Deep Research source inventory and reliability review with private content as the next prompt. Do not use a documentation, curation, rendering, or private content-pack stage to process raw third-party sources into committed data, fetch from the network, use Google Drive storage, run Deep Research, run CUDA, benchmark, execute scored experiments, publicly publish the website, or make solve claims.
Stage 5AN completion handoffs belong under ignored `codex-output/stage5an-codex-completion.md`; Stage 5AN generated content packs belong under ignored `deep-research-content-packs/stage5an/`; Stage 5AN hosted content and combined webroots belong under ignored `website-export/stage5an/`.
Stage 5AC completion handoffs belong under ignored `codex-output/stage5ac-codex-completion.md`.
Stage 5AD completion handoffs belong under ignored `codex-output/stage5ad-codex-completion.md`.
Do not stage the handoff, generated conformance reports, raw data, generated result bodies, SQLite
databases, or local CUDA diagnostics.
