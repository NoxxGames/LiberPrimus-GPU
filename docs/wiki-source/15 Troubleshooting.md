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

## Research Synthesis Validation Fails

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli research-synthesis validate --data-dir data/research --staged-plan docs/roadmap/staged-plan.md
```

If it fails, check that every method-family record has reopen and stop conditions, every retirement
record references a method family, CUDA is still deferred, cookie SHA-256 broadening requires an
explicit new source, and the staged plan still contains its update policy.

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
