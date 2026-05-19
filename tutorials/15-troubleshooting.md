# Troubleshooting

## Purpose

Fix common local setup, data, and validation issues.

## Common Checks

```powershell
git status --short
git remote -v
.\.venv\Scripts\python.exe -m libreprimus.cli smoke
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-state-drift
.\.venv\Scripts\python.exe -m libreprimus.cli research-synthesis validate --data-dir data/research --staged-plan docs/roadmap/staged-plan.md
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-all --allow-warnings
```

## Missing Raw Data

Many CLIs support `--allow-missing` for raw-data-free validation. Missing raw data should not block
CI unless a stage explicitly requires local review.

## Generated Output Appears In Git Status

Check ignore rules:

```powershell
git check-ignore -v experiments/results/discord-promotion/stage3o/promotion_candidates.jsonl
git check-ignore -v experiments/results/discord-lead-promotion/stage3r/promotion_audit_records.jsonl
git check-ignore -v experiments/results/image-transforms/stage3p/review_index.html
git check-ignore -v experiments/results/image-transforms/stage3p/contact_sheets/example.jpg
git check-ignore -v experiments/results/stego/outguess/stage3v/summary.json
git check-ignore -v experiments/results/source-lock-triage/stage4b/source_triage_report.json
git check-ignore -v experiments/results/visual-annotation/stage4c/site/index.html
git check-ignore -v experiments/results/bounded-numeric/stage4d/summary.json
git check-ignore -v experiments/results/source-delta/stage4e/source_delta_report.json
git check-ignore -v experiments/results/stego-fixtures/stage4f/fixture_candidate_report.json
git check-ignore -v experiments/results/cookie-refresh/stage4g/summary.json
git check-ignore -v experiments/results/cpu-batch/stage4h/summary.json
git check-ignore -v experiments/results/scoring-consolidation/stage4i/scorer_inventory.json
git check-ignore -v experiments/results/observation-review/stage4j/review_decision_report.json
git check-ignore -v experiments/results/source-lock-snapshots/stage4k/fetch_report.json
git check-ignore -v third_party/CicadaSolversIddqd/example.jpg
git check-ignore -v third_party/SourceSnapshots/example.html
```

If an ignored Stage 3P transform run leaves local images or HTML under `experiments/results/`, do
not stage them. Re-run the transform command only after confirming raw page images remain ignored.

If an ignored Stage 3Q review-bundle run leaves redacted shards, JSONL indexes, or HTML review
pages under `experiments/results/discord-review-bundles/`, do not stage them. The committed
aggregate is the only Stage 3Q data output intended for the repo.

If a Stage 3R promotion audit leaves JSONL records under
`experiments/results/discord-lead-promotion/`, do not stage them. Commit only the curated YAML
records and disabled manifests.

If a Stage 3S Onion 7 run leaves candidate records under
`experiments/results/post-discord/stage3s/`, do not stage them. Commit only summary docs, tests,
and research logs.

If a Stage 3T GP/rune verifier run leaves verification records under
`experiments/results/post-discord/stage3t/`, do not stage them. Commit only summary docs, tests,
and research logs.

If a Stage 3U cookie signed-variant run leaves hash candidate records under
`experiments/results/post-discord/stage3u/`, do not stage them. Commit only summary docs, tests,
and research logs.

If a Stage 3V OutGuess run leaves extraction records, tool records, synthetic images, or extracted
payloads under `experiments/results/stego/outguess/stage3v/`, do not stage them. Commit only
metadata, manifests, docs, tests, and research logs.

If a Stage 4A Discord full-review build leaves static site files, redacted message streams, channel
shards, topic shards, indexes, copied LP page images, thumbnails, contact sheets, or upload archives
under `experiments/results/discord-full-review/stage4a/`, do not stage them. Commit only aggregate
records, code, schemas, docs, tests, and research logs.

If a Stage 4B source-lock triage run leaves JSON, JSONL, duplicate-link, rejected-link, or warning
files under `experiments/results/source-lock-triage/stage4b/`, do not stage them. Commit only the
curated YAML source/observation/negative-control records, disabled manifests, code, schemas, docs,
tests, and research logs.

If a Stage 4C visual annotation build leaves site pages, copied review images, grid overlays, or
blank templates under `experiments/results/visual-annotation/stage4c/`, do not stage them. Commit
only schemas, code, committed YAML task records, docs, tests, and research logs.

If a Stage 4D bounded numeric verifier run leaves `summary.json`, result JSONL, manifest-status JSONL,
warning JSONL, or negative-control JSONL under `experiments/results/bounded-numeric/stage4d/`, do not
stage them. Commit only schemas, code, docs, tests, and research logs.

If a Stage 4E source-delta audit leaves `path_index.jsonl`, `source_delta_report.json`,
duplicate/unique candidate JSONL files, warnings, temporary clones, or downloaded raw cache contents,
do not stage them. Commit only metadata YAML records, disabled manifests, schemas, code, docs, tests,
and research logs. Font binaries must not be committed or shared.

If a Stage 4F stego/audio fixture source-lock run leaves `fixture_candidate_report.json`,
`source_gap_records.jsonl`, warnings, temporary downloads, or raw cache contents, do not stage them.
Commit only fixture metadata YAML records, disabled manifests, schemas, code, docs, tests, and
research logs. Do not run or stage OutGuess/OpenPuff/MP3Stego outputs, audio scans, binaries,
images, fonts, archives, or extracted payloads.

If a Stage 4G cookie refresh leaves `candidate_records.jsonl`, `exact_matches.jsonl`,
`duplicate_candidates.jsonl`, `summary.json`, or `warnings.jsonl`, do not stage them. Commit only the
aggregate summary YAML, schemas, code, docs, tests, and research log.

If a Stage 4H CPU batch run leaves `result_records.jsonl`, `summary.json`,
`adapter_coverage.json`, or `warnings.jsonl` under `experiments/results/cpu-batch/stage4h/`, do not
stage them. Commit only schemas, manifests, code, docs, tests, research logs, and aggregate summary
YAML. Do not add CUDA code while fixing CPU batch failures.

If a Stage 4I scoring consolidation run leaves `scorer_inventory.json`,
`calibration_report_generated.json`, `cpu_batch_score_compatibility.json`, or `warnings.jsonl`,
do not stage them. Commit only schemas, scoring data records, docs, tests, and research logs.

If a Stage 4J observation review run leaves `review_decision_report.json`,
`quarantine_report.json`, `promotion_gate_report.json`, `path_sanitisation_report.json`, or
`warnings.jsonl`, do not stage them. Commit only schemas, review records, docs, tests, and research
logs.

If a Stage 4K source-lock snapshot build leaves `fetch_report.json`, `rejected_sources.jsonl`,
`duplicate_sources.jsonl`, `warnings.jsonl`, or cached public-source bytes under
`third_party/SourceSnapshots/`, do not stage them. Commit only source-lock metadata, schemas, code,
docs, tests, and research logs.

If a Stage 4L observation-promotion build leaves `promotion_ledger_report.json`,
`manifest_readiness_report.json`, `blocker_report.json`, or `warnings.jsonl`, do not stage them.
Commit only the YAML ledger/readiness/blocker/summary records, schemas, code, docs, tests, and
research logs.

If local deep-research reports appear under `deep-research-reports/`, do not stage them. They are
ignored local review inputs.

## Anti-Drift Check Fails

Run the focused checker:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-state-drift
```

If it fails, update the operational source-of-truth files together: `STATUS.md`, `ROADMAP.md`,
`AGENTS.md`, `README.md`, and `docs/roadmap/staged-plan.md`. Historical references in development logs and research logs do not
need to be rewritten, but current-state claims in long-lived docs must match the latest completed
stage, canonical corpus inactive status, page-boundary review status, CUDA deferral, raw/generated
output policy, Discord privacy, and no-solve-claim policy.

If onboarding map checks fail, confirm that `docs/onboarding/start-here.md`,
`source-of-truth-map.md`, `codex-navigation-map.md`, `deep-research-handoff-map.md`,
`contributor-module-map.md`, and `private-generated-data-map.md` exist and describe the current
Stage 3Z/Stage 4A direction.

After Stage 4L, onboarding and staged-plan checks should show Stage 4L complete and Stage 4M image
source-variant and compression preflight next.

If path sanitisation fails, run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli observation-review check-paths --repo-root .
```

Replace accidental absolute local paths with repository-relative paths. Keep command examples only
when they are explicitly marked as example paths.

## Stage 4A Bundle Or Site Problems

If the Stage 4A static site is missing, rebuild the ignored bundle and validate it:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-full-review build `
  --discord-dir third_party/LiberPrimusDiscordChats `
  --lp-pages-dir third_party/LiberPrimusPages `
  --out-dir experiments/results/discord-full-review/stage4a `
  --privacy-mode redacted_public `
  --include-lp-page-gallery `
  --emit-noindex `
  --emit-robots `
  --allow-warnings

.\.venv\Scripts\python.exe -m libreprimus.cli discord-full-review validate `
  --results-dir experiments/results/discord-full-review/stage4a
```

Do not copy raw Discord HTML or raw LP page images into committed paths to repair a missing site.

If an uploaded Stage 4A site predates the follow-up privacy hardening, reupload the regenerated
`site/` directory so `robots.txt`, noindex metadata, `SITE_PRIVACY_NOTICE.md`,
`SFTP_UPLOAD_CHECKLIST.md`, and `site_manifest.json` are present.

## Research Synthesis Validation Fails

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli research-synthesis validate --data-dir data/research --staged-plan docs/roadmap/staged-plan.md
```

If it fails, check that every method-family record has reopen and stop conditions, every retirement
record references a method family, CUDA is still deferred, cookie SHA-256 broadening requires an
explicit new source, and the staged plan still contains its update policy.

## Stage 4B Source-Lock Validation Fails

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-lock-triage validate `
  --promoted-sources data/observations/archive/stage4b-promoted-source-records.yaml `
  --source-health data/locks/third-party/stage4b-source-health-records.yaml `
  --visual-observations data/observations/visual/stage4b-visual-observation-records.yaml `
  --negative-controls data/observations/research/stage4b-negative-control-records.yaml `
  --cookie-source-records data/observations/web/stage4b-cookie-candidate-source-records.yaml `
  --manifest-dir experiments/manifests/stage4b-disabled
```

Failures usually mean a record is missing `trusted_as_canonical=false`, a visual observation is
marked usable as an experiment seed, a disabled manifest accidentally allows execution, or an
unsafe/private URL was promoted.

## Stage 4C Visual Annotation Validation Fails

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli visual-annotation validate `
  --task data/observations/visual/stage4c-visual-annotation-tasks.yaml `
  --cuneiform data/observations/visual/stage4c-cuneiform-reading-candidates.yaml `
  --dot data/observations/visual/stage4c-dot-pattern-annotation-tasks.yaml `
  --delimiter data/observations/visual/stage4c-delimiter-annotation-tasks.yaml `
  --negative data/observations/visual/stage4c-visual-negative-control-annotation-tasks.yaml `
  --summary data/observations/visual/stage4c-annotation-pack-summary.yaml
```

Failures usually mean a task invented coordinates, marked a reading verified, enabled a reset-boundary
hypothesis, omitted required negative controls, or set `usable_as_experiment_seed=true`.

## CLI Command Missing After Refactor

Run the command-surface tests and inspect the registered groups:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/python/test_stage3x_cli_command_surface.py tests/python/test_stage3x_cli_modularisation.py
.\.venv\Scripts\python.exe -m libreprimus.cli --help
```

Stage 3X keeps `python/libreprimus/cli.py` as the public entrypoint and moves command groups into
`python/libreprimus/cli_commands/`. Do not create `python/libreprimus/cli/` while `cli.py` exists,
and do not rename commands as part of a mechanical modularisation.

## Image Transform Run Is Slow

Stage 3P uses bounded review previews for large images. Do not switch to full-resolution derived
image generation unless a future stage explicitly budgets and scopes that output. Original image
hashes remain anchored by the Stage 3K lock records.

## Discord Review Bundle Is Too Large

Do not concatenate raw Discord HTML files. Rebuild Stage 3Q topic shards and pass only the relevant
redacted shard to a review workflow:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-review build-bundles `
  --ingestion-dir experiments/results/discord-ingestion/stage3n `
  --promotion-dir experiments/results/discord-promotion/stage3o `
  --raw-dir third_party/LiberPrimusDiscordChats `
  --out-dir experiments/results/discord-review-bundles/stage3q `
  --aggregate-out data/observations/discord/discord-review-bundle-aggregate-stage3q.yaml `
  --allow-missing `
  --allow-warnings
```

If a shard still looks too large, split the topic further in code/tests instead of publishing raw
chat logs.

## Stage 3R Manifest Validation Fails

Check that the three post-Discord manifests are disabled:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-leads validate `
  --promoted-sources data/observations/discord/stage3r-promoted-source-records.yaml `
  --promoted-observations data/observations/discord/stage3r-promoted-observation-records.yaml `
  --negative-controls data/observations/discord/stage3r-negative-control-records.yaml `
  --manifest-dir experiments/manifests/post-discord `
  --allow-empty
```

Do not fix validation by enabling execution or removing privacy checks.

## Stage 3S Onion 7 Run Looks Noisy

An inconclusive top score is a valid bounded result. Do not widen Onion 7 value spaces, add
speculative routes, or run other Stage 3R manifests in the same stage. Record the summary and
queue a separate follow-up if review justifies it.

## Stage 3T GP/Rune Claim Missing Spans

`missing_source_span` is a valid verifier result. Do not search nearby spans to make a claim true.
Improve claim extraction or span-linking in a separate bounded follow-up, then rerun the verifier.

## Stage 3U Cookie Pack Has No Exact Match

Zero exact SHA-256 matches is a valid bounded result. Do not add more strings, test partial
matches, or switch algorithms inside the completed run. Queue a new explicit manifest if the
scope changes.

## Stage 4G Cookie Refresh Has No Exact Match

Zero exact matches remains a valid result. The correct follow-up is to update the cookie method
family as negative/deprioritised and move on to Stage 4H unless a later source-lock stage produces
new exact candidate strings. Do not broaden to fuzzy/partial matching, arbitrary strings, hashcat,
GPU/CUDA, dictionaries, or live web/Tor strings.

## Stage 4I Scoring Output Appears In Git Status

Generated scoring consolidation output belongs under ignored
`experiments/results/scoring-consolidation/stage4i/`. Do not stage generated scorer inventories,
rendered calibration reports, CPU batch compatibility JSON, or warning JSONL files.

Committed scoring policy records live under `data/scoring/`. If `libreprimus scoring validate`
fails, fix the committed records or schemas instead of staging generated reports.

## Stage 4J Observation Review Validation Fails

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli observation-review validate `
  --policy data/observations/review/stage4j-observation-review-policy.yaml `
  --decisions data/observations/review/stage4j-observation-review-decisions.yaml `
  --promotions data/observations/review/stage4j-observation-promotion-records.yaml `
  --quarantine data/observations/review/stage4j-observation-quarantine-records.yaml `
  --summary data/observations/review/stage4j-observation-review-summary.yaml
```

Failures usually mean a review state is invalid, a promotion record no longer matches policy gates,
a quarantine record lacks a false-positive rationale, or a record implies a solve/canonical claim.

## A Scoring Label Looks Strong

`positive_control_like`, `plausible_lead`, and `weak_lead` are review priorities only. They are not
solve claims and do not verify plaintext. Use the score to decide what to review, not what to call
solved.

## Stage 3V OutGuess Tool Or Assets Missing

Missing `outguess` or historical fixture assets is a valid harness result when the command uses
`--allow-missing-tool` and `--allow-missing-assets`. Do not install tools automatically or download
archives during validation. Source-lock fixtures in a separate stage.

## Wiki Publish Fails

Validate local Wiki source first:

```powershell
.\scripts\github\validate-wiki-source.ps1
```

If the Wiki remote is unavailable, record the failure in `docs/github/wiki-publish-report.md`.

## Solve Claims

Do not treat terminal output, Discord claims, local review indexes, or generated candidates as solve
evidence. A solve requires a reproducible manifest, pinned corpus, matching output, tests, and
review.
