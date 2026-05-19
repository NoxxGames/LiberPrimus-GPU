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
