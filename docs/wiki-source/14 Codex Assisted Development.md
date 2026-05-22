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
# Stage 4Q Codex Output Boundary

Stage 4Q writes a local completion handoff under `codex-output/`. That directory is ignored and must not be staged. The committed source of truth is the Stage 4Q code, schemas, manifests, docs, and aggregate records under `data/`.

When using Codex after Stage 5Y, cite the Stage 5Y parity-report, result-store integration, score-summary integration, method-status impact, generated-body policy, full-p56 blocker preservation, CUDA contract readiness-gate, bounded scored-experiment readiness, guardrail, next-stage decision, and summary records; the Stage 5X native run, native parity, result-store preflight, score-summary preflight, full-p56 blocker, guardrail, next-stage decision, and summary records; the Stage 5W prime-minus-one source inventory, stream contract, prime schedule, Candidate Batch ABI mapping, native parity preparation, result-store preflight, guardrail, next-stage decision, and summary records; the Stage 5V native adapter, conformance fixture, token-buffer, schedule, score-vector, top-k, result-store, implementation-status, next-stage decision, and summary records; and the Stage 5U Candidate Batch ABI, token-buffer, transform-parameter, key-schedule, stream-schedule, score-vector, top-k, backend-surface, result-store compatibility, ABI gap closure, and next-stage decision records. Also preserve the Stage 5T solved-family inventory/parity matrix/kernel-readiness/ABI-gap/benchmark-readiness/guardrail records, Stage 5S compact integration records, Stage 5R expanded parity records, Stage 5Q candidate mappings, Stage 5O repeat-run/repeat-parity/result-store/score-summary/expansion-decision records, Stage 5N parity-report/gate/boundary/preflight/guardrail records, Stage 5M run/parity/boundary records, Stage 5L token-mapping/native-parity records, Stage 5K Gematria parity-reporting/preflight records, Stage 5J Gematria CUDA kernel records, Stage 5I Gematria CUDA preparation records, Stage 5H Gematria mod-29 `shift_score` contract records, Stage 5G parity-reporting/device-code audit records, Stage 5F synthetic `shift_score_kernel` parity records, Stage 5E selected contract, Stage 4O CPU batch parity expectations, Stage 4P unified result surfaces, Stage 4Q benchmark plans, Stage 5A target-plan/scaffold/gate records, Stage 5B harness/backend/matrix records, Stage 5C build/device records, and Stage 5D native CPU backend/threading records. Do not let ABI, prime-stream contract, no-GPU native parity, or reporting metadata turn into broad CUDA implementation, real Liber Primus CUDA execution, solved or unsolved page CUDA use, GPU benchmarking, generated result-body publication, website expansion, or `codex-output/**` staging without an explicit prompt.

Stage 5V completion handoffs belong under ignored `codex-output/stage5v-codex-completion.md`.
Stage 5W completion handoffs belong under ignored `codex-output/stage5w-codex-completion.md`.
Stage 5X completion handoffs belong under ignored `codex-output/stage5x-codex-completion.md`.
Stage 5Y completion handoffs belong under ignored `codex-output/stage5y-codex-completion.md`.
Do not stage the handoff, generated conformance reports, raw data, generated result bodies, SQLite
databases, or local CUDA diagnostics.
