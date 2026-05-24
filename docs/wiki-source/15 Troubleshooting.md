> This Wiki page mirrors $sourceRel. The repository tutorial file is the source of truth.

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
git check-ignore -v experiments/results/result-store-unification/stage4p/summary.json
git check-ignore -v experiments/results/result-store-unification/stage4p/results.sqlite3
git check-ignore -v experiments/results/cuda-build/stage5c/summary.json
git check-ignore -v experiments/results/native-cpu/stage5d/summary.json
git check-ignore -v experiments/results/cuda-kernel/stage5f/summary.json
git check-ignore -v experiments/results/gematria-solved-fixture-mapping/stage5l/summary.json
git check-ignore -v experiments/results/gematria-solved-fixture-cuda/stage5m/summary.json
git check-ignore -v experiments/results/gematria-solved-fixture-cuda-repeat/stage5o/summary.json
git check-ignore -v experiments/results/gematria-cuda-result-store/stage5p/summary.json
git check-ignore -v experiments/results/gematria-expansion-candidate-mapping/stage5q/summary.json
git check-ignore -v experiments/results/gematria-expanded-cuda-result-store/stage5s/summary.json
git check-ignore -v experiments/results/cuda-candidate-batch-abi-conformance/stage5v/summary.json
git check-ignore -v experiments/results/prime-minus-one-native-contract/stage5w/summary.json
git check-ignore -v experiments/results/prime-minus-one-native-parity/stage5x/summary.json
git check-ignore -v experiments/results/prime-minus-one-native-reporting/stage5y/summary.json
git check-ignore -v experiments/results/prime-minus-one-cuda-contract/stage5z/summary.json
git check-ignore -v experiments/results/prime-minus-one-cuda-synthetic/stage5aa/summary.json
git check-ignore -v experiments/results/prime-minus-one-bounded-p56-cuda-parity/stage5ad/summary.json
git check-ignore -v experiments/results/prime-minus-one-bounded-p56-mismatch/stage5ad-fix/summary.json
git check-ignore -v experiments/results/prime-minus-one-bounded-p56-corrected-reporting/stage5ae/summary.json
git check-ignore -v codex-output/stage5c-codex-completion.md
git check-ignore -v codex-output/stage5d-codex-completion.md
git check-ignore -v codex-output/stage5f-codex-completion.md
git check-ignore -v codex-output/stage5g-codex-completion.md
git check-ignore -v codex-output/stage5l-codex-completion.md
git check-ignore -v codex-output/stage5m-codex-completion.md
git check-ignore -v codex-output/stage5p-codex-completion.md
git check-ignore -v codex-output/stage5s-codex-completion.md
git check-ignore -v codex-output/stage5v-codex-completion.md
git check-ignore -v codex-output/stage5w-codex-completion.md
git check-ignore -v codex-output/stage5x-codex-completion.md
git check-ignore -v codex-output/stage5y-codex-completion.md
git check-ignore -v codex-output/stage5z-codex-completion.md
git check-ignore -v codex-output/stage5aa-codex-completion.md
git check-ignore -v codex-output/stage5ad-fix-codex-completion.md
git check-ignore -v codex-output/stage5ae-codex-completion.md
git check-ignore -v codex-output/stage5af-codex-completion.md
git check-ignore -v codex-output/stage5ai-codex-completion.md
git check-ignore -v codex-output/stage5aj-codex-completion.md
git check-ignore -v codex-output/stage5ak-codex-completion.md
git check-ignore -v experiments/results/source-harvester/stage5af/summary.json
git check-ignore -v experiments/results/source-harvester-local/stage5ag/summary.json
git check-ignore -v experiments/results/research-bundles/stage5ai/summary.json
git check-ignore -v experiments/results/source-harvester-usefulfiles/stage5aj/important_links_url_index.json
git check-ignore -v experiments/results/source-harvester-community-facts/stage5ak/community_claim_records.jsonl
git check-ignore -v third_party/example.zip
git check-ignore -v third_party/UsefulFilesAndIdeas/LP\ Excel.xlsx
git check-ignore -v third_party/UsefulFilesAndIdeas/community-facts/community-facts-collection.txt
git check-ignore -v third_party/UsefulFilesAndIdeas/community-facts/1.webp
git check-ignore -v source-harvester-output/example.txt
git check-ignore -v harvest-output/example.txt
git check-ignore -v research-inputs/example.txt
git check-ignore -v research-inputs/stage5ai/master_manifest.yaml
git check-ignore -v research-inputs/stage5aj/master_manifest.yaml
git check-ignore -v research-inputs/stage5ak/community_claim_records.jsonl
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

If a Stage 5D native CPU run leaves `native_backend_capabilities.json`,
`threading_parity_report.json`, `native_python_parity_report.json`, `native_cpu_diagnostics.json`,
`summary.json`, or `warnings.jsonl` under `experiments/results/native-cpu/stage5d/`, do not stage
them. Commit only schemas, code, manifests, compact YAML records, docs, tests, and research logs.
Do not treat timing diagnostics as benchmarks or speedup evidence.

If a Stage 4J observation review run leaves `review_decision_report.json`,
`quarantine_report.json`, `promotion_gate_report.json`, `path_sanitisation_report.json`, or
`warnings.jsonl`, do not stage them. Commit only schemas, review records, docs, tests, and research
logs.

If a Stage 4K source-lock snapshot build leaves `fetch_report.json`, `rejected_sources.jsonl`,
`duplicate_sources.jsonl`, `warnings.jsonl`, or cached public-source bytes under
`third_party/SourceSnapshots/`, do not stage them. Commit only source-lock metadata, schemas, code,
docs, tests, and research logs.

If a Stage 5AF source-harvester run leaves `harvest_plan.json`, `source_manifest_validation.json`,
`dry_run_summary.json`, `research_bundle_plan.json`, `failures.jsonl`, `summary.json`,
`warnings.jsonl`, or research-bundle preview scaffolds under
`experiments/results/source-harvester/stage5af/`, do not stage them. Commit only source-harvester
schemas, manifests, code, compact data records, docs, tests, and research logs. Raw harvester
outputs belong in ignored local roots such as `source-harvester-output/`, `harvest-output/`, or
`research-inputs/`; Google/Dropbox/Colab sources are manual-export local inputs, and Google Drive
is not project storage. If a Stage 5AG local inventory leaves full inventories under
`experiments/results/source-harvester-local/stage5ag/`, do not stage them. Commit only compact
metadata under `data/source-harvester/stage5ag-*`, schemas, docs, tests, and source code.

If a Stage 5AI curated-bundle run leaves `master_manifest.yaml`, bundle manifests, source cards,
content indexes, extracted text snippets, website-ingest indexes, Deep-Research pack indexes,
missing-source records, or warning reports under `research-inputs/stage5ai/` or
`experiments/results/research-bundles/stage5ai/`, do not stage them. Commit only compact metadata
under `data/source-harvester/stage5ai-*`, schemas, docs, tests, source code, and README/.gitkeep
scaffolds.

If a Stage 5AJ UsefulFilesAndIdeas run leaves workbook-cell indexes, important-link indexes,
source-manifest previews, bundle bodies, source cards, content indexes, policy reports, summaries,
or warning reports under `research-inputs/stage5aj/`,
`experiments/results/research-bundles/stage5aj/`, or
`experiments/results/source-harvester-usefulfiles/stage5aj/`, do not stage them. Commit only compact
metadata under `data/source-harvester/stage5aj-*`, schemas, docs, tests, source code, and
`.gitkeep` scaffolds. Do not stage raw `third_party/UsefulFilesAndIdeas/` workbooks, images, or
text files.

If a Stage 5AK community-facts run leaves message indexes, ordered attachment indexes, source cards,
content indexes, claim records, correction logs, arithmetic-preflight reports, bundle addenda,
summaries, or warning reports under `research-inputs/stage5ak/`,
`experiments/results/research-bundles/stage5ak/`, or
`experiments/results/source-harvester-community-facts/stage5ak/`, do not stage them. Commit only
compact metadata under `data/source-harvester/stage5ak-*`, schemas, docs, tests, source code, and
`.gitkeep` scaffolds. Do not stage raw `third_party/UsefulFilesAndIdeas/community-facts/` message
logs or images, and do not treat community-facts claim records as source truth or solve evidence.

If a Stage 4L observation-promotion build leaves `promotion_ledger_report.json`,
`manifest_readiness_report.json`, `blocker_report.json`, or `warnings.jsonl`, do not stage them.
Commit only the YAML ledger/readiness/blocker/summary records, schemas, code, docs, tests, and
research logs.

If a Stage 4M image-preflight build leaves `image_metadata.jsonl`, `compression_metrics.jsonl`,
`source_variant_preflight.jsonl`, `artifact_candidate_report.jsonl`, `summary.json`, or
`warnings.jsonl`, do not stage them. Commit only the YAML preflight/readiness records, schemas,
code, docs, tests, and research logs. Raw LP images and `data/raw/images/Fib421.jpg` remain ignored.

If a Stage 4N stego/audio positive-control build leaves `readiness_report.json`,
`cache_report.json`, `toolchain_report.json`, or `warnings.jsonl`, do not stage them. Commit only
the YAML readiness/cache/expected-output/toolchain/summary records, schemas, code, docs, tests, and
research logs. Ignored cache files under `third_party/StegoPositiveControls/`, historical fixture
artefacts, and extracted payloads remain outside Git.

If a Stage 4O CPU batch adapter build leaves `result_records.jsonl`, `adapter_coverage.json`,
`parity_expectations.jsonl`, `scoring_compatibility.json`, `summary.json`, or `warnings.jsonl`, do
not stage them. Commit only schemas, manifests, CPU batch code, tests, docs, research logs, and the
aggregate YAML summary under `data/research/`.

If a Stage 4P result-store unification run leaves `source_inventory.json`,
`unified_result_records.jsonl`, `unified_score_summary_records.jsonl`, `method_status_join.json`,
`cross_stage_report.json`, `summary.json`, `warnings.jsonl`, or SQLite files under
`experiments/results/result-store-unification/stage4p/`, do not stage them. Commit only schemas,
manifests, result-store code, tests, docs, research logs, and the aggregate YAML summary under
`data/research/`.

If a Stage 5W prime-minus-one native contract run leaves source inventory, stream contract, prime
schedule, Candidate Batch ABI mapping, native parity preparation, result-store preflight, guardrail,
next-stage decision, summary, or warning reports under
`experiments/results/prime-minus-one-native-contract/stage5w/`, do not stage them. Commit only
schemas, manifests, code, compact YAML records, docs, tests, and research logs. Do not invent p56
token buffers while fixing validation failures.

If a Stage 5X prime-minus-one native parity run leaves native run, native parity, result-store
preflight, score-summary preflight, full-p56 blocker, guardrail, next-stage decision, summary, or
warning reports under `experiments/results/prime-minus-one-native-parity/stage5x/`, do not stage
them. Commit only schemas, manifests, code, compact YAML records, docs, tests, and research logs.
Do not execute the blocked full-p56 mapping while fixing validation failures.

If a Stage 5Y prime-minus-one native reporting run leaves parity report, result-store integration,
score-summary integration, method-status impact, generated-body policy, full-p56 blocker
preservation, CUDA contract readiness-gate, scored-experiment readiness, guardrail, next-stage
decision, summary, or warning reports under
`experiments/results/prime-minus-one-native-reporting/stage5y/`, do not stage them. Commit only
schemas, manifests, code, compact YAML records, docs, tests, and research logs. Do not rerun native
parity, run CUDA, modify CUDA source, add kernels, execute the blocked full-p56 mapping, or treat
reporting metadata as solve evidence while fixing validation failures.

If a Stage 5AA prime-minus-one CUDA synthetic parity run leaves kernel-build, CUDA-run, parity,
device-subset, result-store preflight, p56 blocker, scored-experiment deferral, next-stage decision,
summary, or warning reports under
`experiments/results/prime-minus-one-cuda-synthetic/stage5aa/`, do not stage them. Commit only
schemas, manifests, code, compact YAML records, docs, tests, and research logs. Do not run p56 or
full-p56 CUDA, unsolved pages, scored experiments, benchmarks, website expansion, raw data, or
method-status upgrades while fixing validation failures.

If a Stage 5C CUDA build/device run leaves `toolchain_detection_report.json`,
`device_detection_report.json`, `smoke_build_report.json`, `summary.json`, `warnings.jsonl`, or
CMake build directories under `experiments/results/cuda-build/stage5c/`, do not stage them.
Commit only schemas, manifests, CUDA build/device code, tests, docs, research logs, and compact
YAML records under `data/cuda/`. A failed optional local smoke build is readiness metadata only;
do not treat it as CUDA parity or benchmark evidence.

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

After Stage 5Q, onboarding and staged-plan checks should show Stage 5Q complete and Stage 5R
controlled solved-fixture CUDA result-store integration next.

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
# Stage 4Q Benchmark Planning Troubleshooting

If Stage 4Q validation fails, regenerate raw-data-free diagnostics with:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli benchmark-planning build-plan `
  --manifest experiments/manifests/benchmarks/stage4q-cuda-parity-readiness.yaml `
  --plan-out data/benchmarks/stage4q-cpu-benchmark-plan.yaml `
  --readiness-out data/benchmarks/stage4q-cuda-parity-readiness.yaml `
  --summary-out data/research/stage4q-cpu-benchmark-parity-planning-summary.yaml `
  --out-dir experiments/results/benchmarks/stage4q `
  --allow-warnings
```

Do not stage `experiments/results/benchmarks/stage4q/` or `codex-output/`.

# Stage 5B CUDA Parity Harness Troubleshooting

If Stage 5B validation fails, rerun the committed-record check:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-parity validate-stage5b `
  --harness-plan data/cuda/stage5b-cuda-parity-harness-plan.yaml `
  --parity-fixtures data/cuda/stage5b-cuda-parity-fixtures.yaml `
  --backend-capability data/cuda/stage5b-cuda-backend-capability.yaml `
  --future-kernel-matrix data/cuda/stage5b-future-kernel-parity-matrix.yaml `
  --summary data/cuda/stage5b-cuda-parity-harness-summary.yaml `
  --results-dir experiments/results/cuda-parity/stage5b
```

Generated Stage 5B reports belong under ignored `experiments/results/cuda-parity/stage5b/`.
Do not stage `harness_plan_report.json`, `parity_fixtures_report.json`,
`backend_capability_report.json`, `future_kernel_parity_matrix_report.json`, `summary.json`, or
`warnings.jsonl`.

If local CUDA tools are present, they may be recorded as optional capability metadata only. Stage
5B must still pass without CUDA hardware, must not add `.cu` or `.cuh` implementation changes, and
must not record performance or speedup claims. Keep the local Codex completion handoff under
ignored `codex-output/stage5b-codex-completion.md`.

# Stage 5H Gematria Shift Contract Troubleshooting

If Stage 5H validation fails, rebuild the committed records from the no-GPU manifests:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-shift-contract build-contract `
  --manifest experiments/manifests/cuda/stage5h-gematria-shift-score-contract.yaml `
  --contract-out data/cuda/stage5h-gematria-shift-score-contract.yaml `
  --out-dir experiments/results/gematria-shift-contract/stage5h `
  --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-shift-contract build-summary `
  --contract data/cuda/stage5h-gematria-shift-score-contract.yaml `
  --native-fixtures data/cuda/stage5h-gematria-native-parity-fixtures.yaml `
  --solved-fixture-mapping data/cuda/stage5h-gematria-solved-fixture-safe-mapping.yaml `
  --score-summary-plan data/cuda/stage5h-gematria-score-summary-parity-plan.yaml `
  --summary-out data/cuda/stage5h-gematria-shift-contract-summary.yaml `
  --out-dir experiments/results/gematria-shift-contract/stage5h `
  --allow-warnings
```

Generated Stage 5H reports belong under ignored
`experiments/results/gematria-shift-contract/stage5h/`, and the Codex completion handoff belongs
under ignored `codex-output/stage5h-codex-completion.md`. Stage 5H must not add CUDA kernels,
execute CUDA, process real Liber Primus data through CUDA, or record performance claims.

# Stage 5I Gematria CUDA Prep Troubleshooting

If Stage 5I validation fails, rebuild the committed preparation records from the no-GPU manifests:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-prep build-kernel-preparation `
  --manifest experiments/manifests/cuda/stage5i-gematria-cuda-kernel-preparation.yaml `
  --preparation-out data/cuda/stage5i-gematria-cuda-kernel-preparation.yaml `
  --out-dir experiments/results/gematria-cuda-prep/stage5i `
  --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-prep build-summary `
  --preparation data/cuda/stage5i-gematria-cuda-kernel-preparation.yaml `
  --abi-plan data/cuda/stage5i-gematria-cuda-abi-plan.yaml `
  --validation-vectors data/cuda/stage5i-gematria-cuda-validation-vectors.yaml `
  --implementation-checklist data/cuda/stage5i-gematria-cuda-implementation-checklist.yaml `
  --summary-out data/cuda/stage5i-gematria-cuda-preparation-summary.yaml `
  --out-dir experiments/results/gematria-cuda-prep/stage5i `
  --allow-warnings
```

Generated Stage 5I reports belong under ignored `experiments/results/gematria-cuda-prep/stage5i/`,
and the Codex completion handoff belongs under ignored `codex-output/stage5i-codex-completion.md`.
Stage 5I must not add CUDA source files, add kernels, run CUDA transforms, run solved or unsolved
page data through CUDA, process real Liber Primus CUDA data, or record performance claims.

# Stage 5J Gematria CUDA Kernel Troubleshooting

If Stage 5J validation fails, rebuild or inspect the committed kernel records:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-kernel validate-stage5j `
  --implementation data/cuda/stage5j-gematria-cuda-kernel-implementation.yaml `
  --build-records data/cuda/stage5j-gematria-cuda-kernel-build-records.yaml `
  --parity-records data/cuda/stage5j-gematria-cuda-synthetic-parity-records.yaml `
  --summary data/cuda/stage5j-gematria-cuda-kernel-summary.yaml `
  --results-dir experiments/results/gematria-cuda-kernel/stage5j
```

No-GPU CI may record skipped build/parity status. Local CUDA parity may pass when the toolkit and
device are available. Do not treat either path as a benchmark, speedup claim, or permission to run
real Liber Primus data through CUDA.

# Stage 5K Gematria CUDA Parity Reporting Troubleshooting

If Stage 5K validation fails, rebuild or inspect the committed parity-reporting records:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-parity-reporting validate-stage5k `
  --parity-report data/cuda/stage5k-gematria-cuda-parity-report.yaml `
  --device-code-audit data/cuda/stage5k-gematria-cuda-device-code-audit.yaml `
  --preflight data/cuda/stage5k-gematria-solved-fixture-safe-preflight.yaml `
  --score-summary-preflight data/cuda/stage5k-gematria-cuda-score-summary-preflight.yaml `
  --summary data/cuda/stage5k-gematria-cuda-parity-reporting-summary.yaml `
  --results-dir experiments/results/gematria-cuda-parity-reporting/stage5k
```

Stage 5K reports the Stage 5J synthetic hash match and records blockers. It must not add CUDA
source, run CUDA, run solved or unsolved page data through CUDA, run GPU benchmarks, publish
generated reports, or claim a solve. If solved-fixture-safe records are not ready, the expected next
work is Stage 5L token mapping and native parity fixture preparation.

# Stage 5L Solved-Fixture Mapping Troubleshooting

If Stage 5L validation fails, rebuild or inspect the committed mapping records:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-mapping validate-stage5l `
  --token-mapping data/cuda/stage5l-gematria-solved-fixture-token-mapping.yaml `
  --native-parity data/cuda/stage5l-gematria-solved-fixture-native-parity.yaml `
  --output-hash-contract data/cuda/stage5l-gematria-solved-fixture-output-hash-contract.yaml `
  --score-summary-shape data/cuda/stage5l-gematria-solved-fixture-score-summary-shape.yaml `
  --summary data/cuda/stage5l-solved-fixture-token-mapping-summary.yaml `
  --results-dir experiments/results/gematria-solved-fixture-mapping/stage5l
```

Stage 5L records token buffers and native output-token hashes only. It must not add CUDA source,
run CUDA, run solved or unsolved page data through CUDA, run GPU benchmarks, publish generated
reports, or claim a solve. The expected next work is an explicit future Stage 5M solved-fixture-safe
CUDA parity run only if approval and no-unsolved guardrails are present.

# Stage 5M Solved-Fixture CUDA Parity Troubleshooting

If Stage 5M validation fails, inspect the committed run, parity, boundary, and summary records:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-cuda validate-stage5m `
  --run-records data/cuda/stage5m-gematria-solved-fixture-cuda-run.yaml `
  --parity-records data/cuda/stage5m-gematria-solved-fixture-cuda-parity.yaml `
  --boundaries data/cuda/stage5m-gematria-solved-fixture-cuda-boundaries.yaml `
  --summary data/cuda/stage5m-solved-fixture-cuda-parity-summary.yaml `
  --results-dir experiments/results/gematria-solved-fixture-cuda/stage5m
```

Stage 5M may use only the existing `gematria_mod29_shift_score_kernel` over the exact five Stage
5L mapped token buffers. It must not add kernels, change device arithmetic, run real Liber Primus
data through CUDA, run unsolved pages, publish generated reports, run benchmarks, claim speedups, or
claim a solve.

# Stage 5N CUDA Reporting Troubleshooting

If Stage 5N validation fails, rebuild the reporting sequence from committed Stage 5M records and
then run `libreprimus gematria-solved-fixture-cuda-reporting validate-stage5n`. Do not rerun CUDA,
modify CUDA source, add kernels, or process raw data to repair a reporting-only failure.

# Stage 5O CUDA Repeat Troubleshooting

If Stage 5O validation fails, rebuild the repeat records from committed Stage 5M/5L records and
rerun `libreprimus gematria-solved-fixture-cuda-repeat validate-stage5o`. CI/temp repair paths
should use `run-repeat-verification --skip-run`; local CUDA repeat runs may only use the exact
Stage 5M five-buffer pack. Do not add kernels, modify CUDA source, run benchmarks, publish
generated reports, or process unsolved data to repair Stage 5O records.

# Stage 5R Expanded CUDA Parity Troubleshooting

If Stage 5R validation fails, rebuild the sequence from committed Stage 5Q records and rerun
`libreprimus gematria-expanded-solved-fixture-cuda validate-stage5r`. CI/temp repair paths should
use `run-cuda-parity --skip-run`; local CUDA runs may only use `p57-parable`, `some-wisdom`, and
`the-loss-of-divinity`. Do not add kernels, modify device arithmetic, run benchmarks, publish
generated reports, or process unsolved data to repair Stage 5R records.

# Stage 5T CUDA Solved-Family Readiness Troubleshooting

If Stage 5T validation fails, rebuild the metadata sequence and rerun
`libreprimus cuda-solved-family-readiness validate-stage5t`. Do not run CUDA, native/CUDA CMake,
benchmarks, solved fixtures, or unsolved pages to repair readiness records.

Expected Stage 5T counts are 8 solved-family inventory records, 8 parity matrix records, 7
kernel-readiness records, 5 batch ABI gap records, 3 benchmark-readiness records, 6 no-unsolved
guardrail records, and 5 next-stage decision records. The selected next prompt should remain
Stage 5U unified candidate batch ABI consolidation unless the committed readiness records change
under an explicit future stage.

# Stage 5U Candidate Batch ABI Troubleshooting

If Stage 5U validation fails, rebuild the no-GPU metadata sequence and rerun
`libreprimus cuda-candidate-batch-abi validate-stage5u`. Do not run CUDA, native/CUDA CMake,
benchmarks, solved fixtures, or unsolved pages to repair ABI contract records.

Expected Stage 5U counts are 1 candidate-batch ABI record, 8 token-buffer contract records, 6
transform-parameter contract records, 2 key-schedule contract records, 2 stream-schedule contract
records, 7 score-vector contract records, 1 top-k output contract record, 7 backend-surface
contract records, 3 result-store compatibility records, 5 ABI gap closure records, and 9
next-stage decision records. Stage 5U selected Stage 5V native candidate batch ABI reference
adapter and conformance fixtures; Stage 5V has since superseded that next-stage decision with
Stage 5W prime-minus-one stream native parity contract preparation.

Generated Stage 5U reports belong under ignored
`experiments/results/cuda-candidate-batch-abi/stage5u/`, and the local handoff belongs under ignored
`codex-output/stage5u-codex-completion.md`. Do not stage generated reports, generated result bodies,
SQLite files, raw data, or local CUDA diagnostics.

# Stage 5V Native Candidate Batch ABI Conformance Troubleshooting

If Stage 5V validation fails, rebuild the no-GPU conformance sequence and rerun
`libreprimus native-candidate-batch-conformance validate-stage5v`. Do not run CUDA,
native/CUDA CMake, benchmarks, solved fixtures, or unsolved pages to repair conformance records.

Expected Stage 5V counts are 2 native adapter records, 7 conformance fixture records, 3 executed
Python reference fixtures, 4 shape-only fixtures, 7 token-buffer conformance records, 2 schedule
conformance records, 7 score-vector conformance records, 1 top-k conformance record, 3 result-store
conformance records, 8 implementation-status records, and 9 next-stage decision records. The
historical selected next prompt was Stage 5W prime-minus-one stream native parity contract
preparation; Stage 5W through Stage 5Y have since superseded that decision with Stage 5Z
prime-minus-one CUDA contract preparation.

Generated Stage 5V reports belong under ignored
`experiments/results/cuda-candidate-batch-abi-conformance/stage5v/`, and the local handoff belongs
under ignored `codex-output/stage5v-codex-completion.md`. Do not stage generated reports, generated
result bodies, SQLite files, raw data, or local CUDA diagnostics.

# Stage 5X Prime-Minus-One Native Parity Troubleshooting

If Stage 5X validation fails, rebuild the no-GPU prime-minus-one native parity sequence and rerun
`libreprimus prime-minus-one-native-parity validate-stage5x`. Do not run CUDA, native/CUDA CMake,
benchmarks, solved-page expansion, unsolved pages, or the blocked full p56 mapping to repair the
records.

Expected Stage 5X counts are 3 native run records, 3 native parity records, 3 result-store preflight
records, 3 score-summary preflight records, 1 full-p56 blocker record, 7 guardrail records, and 9
next-stage decision records. The selected next prompt should remain Stage 5Y prime-minus-one native
parity reporting and CUDA contract readiness gate unless an explicit future stage changes the
committed decision records.

Generated Stage 5X reports belong under ignored
`experiments/results/prime-minus-one-native-parity/stage5x/`, and the local handoff belongs under
ignored `codex-output/stage5x-codex-completion.md`. Do not stage generated reports, generated
result bodies, SQLite files, raw data, or local CUDA diagnostics.

# Stage 5Y Prime-Minus-One Native Reporting Troubleshooting

If Stage 5Y validation fails, rebuild the reporting sequence from committed Stage 5X records and
rerun `libreprimus prime-minus-one-native-reporting validate-stage5y`. Do not rerun native parity,
run CUDA, native/CUDA CMake, benchmarks, full p56, solved-page expansion, or unsolved pages to
repair the records.

Expected Stage 5Y counts are 3 parity report records, 3 result-store integration records, 3
score-summary integration records, 5 method-status impact records, 7 generated-body policy records,
1 full-p56 blocker preservation record, 1 CUDA contract readiness-gate record, 6 bounded
scored-experiment readiness records, 9 guardrail records, and 10 next-stage decision records. The
selected next prompt should remain Stage 5Z prime-minus-one CUDA contract preparation unless an
explicit future stage changes the committed decision records.

Generated Stage 5Y reports belong under ignored
`experiments/results/prime-minus-one-native-reporting/stage5y/`, and the local handoff belongs
under ignored `codex-output/stage5y-codex-completion.md`. Do not stage generated reports, generated
result bodies, SQLite files, raw data, or local CUDA diagnostics.

# Stage 5AA Prime-Minus-One CUDA Synthetic Troubleshooting

If Stage 5AA validation fails, rebuild the synthetic-only record sequence and rerun
`libreprimus prime-minus-one-cuda-synthetic validate-stage5aa`. Only the
`stage5z-validation-synthetic-prime-control-v0` vector is in scope; do not run p56/full-p56 CUDA,
unsolved pages, scored experiments, benchmarks, website expansion, or raw data to repair the
records.

Expected Stage 5AA counts are 1 kernel implementation record, 1 CUDA run record, 1 parity record,
1 device-subset audit record, 2 result-store preflight records, 2 p56/full-p56 blocker records, 6
scored-experiment deferral records, and 4 next-stage decision records. Stage 5AA historical decision
records may still name the Stage 5AB reporting/preflight follow-up, but operational docs after the
Stage 5AB quality gate select Stage 5AC from the Stage 5AA outcome after stale-doc repair.

Generated Stage 5AA reports belong under ignored
`experiments/results/prime-minus-one-cuda-synthetic/stage5aa/`, and the local handoff belongs under
ignored `codex-output/stage5aa-codex-completion.md`. Do not stage generated reports, generated
result bodies, SQLite files, raw data, or local CUDA diagnostics.

# Stage 5AD Bounded P56 CUDA Parity Troubleshooting

If Stage 5AD validation fails, rebuild the bounded record sequence and rerun
`libreprimus bounded-p56-cuda-parity validate-stage5ad`. The only execution-scoped vector is
`stage5z-validation-p56-bounded-v0`; do not widen to full p56, unsolved pages, scored experiments,
benchmarks, website expansion, raw data, or new kernels to repair the records.

The local Stage 5AD outcome is `failed_hash_mismatch`: expected
`4a3059f12c0f8450bd4ef7e31bf879fbc104202e5fb0e53b7ba514241f07cd87`, computed CUDA hash
`6034fe2431159615449db79c36869236d306768414038314d47d6d57d9ae7387`. That should select
Stage 5AD-fix bounded p56 CUDA parity mismatch investigation, not Stage 5AE reporting.

Generated Stage 5AD reports belong under ignored
`experiments/results/prime-minus-one-bounded-p56-cuda-parity/stage5ad/`, and the local handoff
belongs under ignored `codex-output/stage5ad-codex-completion.md`. Do not stage generated reports,
generated result bodies, build directories, SQLite files, raw data, or local CUDA diagnostics.

# Stage 5AB/5AH/5AI Document Staleness Troubleshooting

If Stage 5AK or later doc-staleness validation fails after updating operational docs, inspect
`data/project-state/stage5ah-doc-staleness-source-of-truth.yaml`, `data/project-state/operational-file-map.yaml`,
`STATUS.md`, `ROADMAP.md`, `AGENTS.md`, `README.md`, and `docs/roadmap/staged-plan.md` for mismatched latest or next
stage labels. After Stage 5AN, the active source-of-truth expects Stage 5AN as latest completed and Stage 5AO as the next Deep Research source inventory stage with private content.

If Stage 5AC bounded-p56 preflight is not ready, do not run p56 CUDA. Keep full p56 blocked, inspect the Stage 5AA
synthetic hash match and Stage 5AB doc-staleness record, then repair metadata before selecting any future bounded
p56 CUDA run.

If operational Markdown drifts, run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-doc-staleness --source-of-truth data/project-state/stage5ah-doc-staleness-source-of-truth.yaml --strict

.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-stage-ledger-staleness `
  --expected-latest-stage "Stage 5AN" `
  --expected-next-stage "Stage 5AO"

.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-operational-file-map-coverage

.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-current-next-stage-consistency `
  --expected-latest-stage "Stage 5AN" `
  --expected-next-stage "Stage 5AO"
```

The checks scan the operational file map, ignore historical logs, reject active Stage 6 website
deferrals, reject stale current/next-stage labels, reject stale stage-ledger truncation, and reject
brittle current CUDA boundary caps that omit the latest completed stage. Generated Stage 5AH
staleness reports belong under ignored `experiments/results/doc-staleness/stage5ah/`, generated
Stage 5AI bundle reports belong under ignored `experiments/results/research-bundles/stage5ai/`,
Stage 5AJ UsefulFiles reports belong under ignored
`experiments/results/source-harvester-usefulfiles/stage5aj/`, and the local Stage 5AJ handoff
belongs under ignored `codex-output/stage5aj-codex-completion.md`. Stage 5AK community-facts
reports belong under ignored `experiments/results/source-harvester-community-facts/stage5ak/`,
generated private bundle bodies belong under ignored `research-inputs/stage5ak/`, and the local
Stage 5AK handoff belongs under ignored `codex-output/stage5ak-codex-completion.md`.

For Stage 5AL website-ingest runs, committed files belong under `data/website-ingest/stage5al/`
and `data/source-harvester/stage5al-*`. Generated private export helpers belong under ignored
`research-inputs/stage5al/`, generated reports belong under ignored
`experiments/results/website-ingest/stage5al/`, and the Codex completion handoff belongs under
ignored `codex-output/stage5al-codex-completion.md`.

For Stage 5AM website-render runs, committed files belong under `data/website-render/stage5am-*`.
Generated static site files and the optional ZIP belong under ignored `website-export/stage5am/`,
renderer reports belong under ignored `experiments/results/website-render/stage5am/`, and the
Codex completion handoff belongs under ignored `codex-output/stage5am-codex-completion.md`.
Confirm ignore coverage with:

```powershell
git check-ignore -v website-export/stage5am/research-index/index.html
git check-ignore -v website-export/stage5am/research-index.zip
git check-ignore -v experiments/results/website-render/stage5am/summary.json
git check-ignore -v codex-output/stage5am-codex-completion.md
```

For Stage 5AN private content-pack runs, committed files belong under `data/deep-research-export/stage5an-*`.
Generated private pack files and ZIP archives belong under ignored `deep-research-content-packs/stage5an/`;
hosted private-content files, combined webroots, and upload ZIP archives belong under ignored
`website-export/stage5an/`; and the Codex completion handoff belongs under ignored
`codex-output/stage5an-codex-completion.md`. Confirm ignore coverage with:

```powershell
git check-ignore -v deep-research-content-packs/stage5an/deep-research-content-pack-stage5an.zip
git check-ignore -v website-export/stage5an/private-content/index.html
git check-ignore -v website-export/stage5an/webserver-root/index.html
git check-ignore -v website-export/stage5an/webserver-root/private-content/index.html
git check-ignore -v website-export/stage5an/webserver-root.zip
git check-ignore -v codex-output/stage5an-codex-completion.md
```
