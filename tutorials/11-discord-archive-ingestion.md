# Discord Archive Ingestion

## Purpose

Scan admin-provided local Discord HTML exports as source-discovery material only.

Stage 4A is planned as full Discord research-bundle extraction for Deep Research. It should build
redacted, scoped, image-aware bundles from local HTML exports without publishing raw logs or private
attachments.

## Commands

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-ingest scan `
  --source-dir third_party/LiberPrimusDiscordChats `
  --out-dir experiments/results/discord-ingestion/stage3n `
  --allow-missing `
  --allow-warnings

.\.venv\Scripts\python.exe -m libreprimus.cli discord-promote promote `
  --ingestion-dir experiments/results/discord-ingestion/stage3n `
  --out-dir experiments/results/discord-promotion/stage3o `
  --promoted-links-out data/observations/discord/promoted-public-source-links-stage3o.yaml `
  --promoted-methods-out data/observations/discord/promoted-method-claim-candidates-stage3o.yaml `
  --promoted-numerics-out data/observations/discord/promoted-numeric-observation-candidates-stage3o.yaml `
  --allow-missing `
  --allow-warnings

.\.venv\Scripts\python.exe -m libreprimus.cli discord-review build-bundles `
  --ingestion-dir experiments/results/discord-ingestion/stage3n `
  --promotion-dir experiments/results/discord-promotion/stage3o `
  --raw-dir third_party/LiberPrimusDiscordChats `
  --out-dir experiments/results/discord-review-bundles/stage3q `
  --aggregate-out data/observations/discord/discord-review-bundle-aggregate-stage3q.yaml `
  --allow-missing `
  --allow-warnings

.\.venv\Scripts\python.exe -m libreprimus.cli discord-leads promote `
  --review-dir experiments/results/discord-review-bundles/stage3q `
  --stage3o-links data/observations/discord/promoted-public-source-links-stage3o.yaml `
  --stage3o-methods data/observations/discord/promoted-method-claim-candidates-stage3o.yaml `
  --stage3o-numerics data/observations/discord/promoted-numeric-observation-candidates-stage3o.yaml `
  --source-registry data/observations/archive/source-archive-records-v0.yaml `
  --visual-registry data/observations/visual/visual-numeric-observations-v0.yaml `
  --cookie-records data/observations/web/cookie-hash-records-v0.yaml `
  --out-dir experiments/results/discord-lead-promotion/stage3r `
  --promoted-sources-out data/observations/discord/stage3r-promoted-source-records.yaml `
  --promoted-observations-out data/observations/discord/stage3r-promoted-observation-records.yaml `
  --negative-controls-out data/observations/discord/stage3r-negative-control-records.yaml `
  --audit-summary-out data/observations/discord/stage3r-promotion-audit-summary.yaml `
  --allow-missing `
  --allow-warnings
```

## Expected Outputs

Ingestion writes ignored extraction JSONL and a local review index. Promotion writes capped,
redacted YAML records for public review. Stage 3Q review bundles write redacted topic shards and
indexes under `experiments/results/discord-review-bundles/stage3q/`; those files are for local
review and are ignored by Git. Stage 3R promotes corroborated public links and exact observation
leads into committed redacted records, preserves negative controls, and creates disabled
post-Discord manifests. Stage 3S executes only the Onion 7 seed-pack manifest, Stage 3T
executes only the GP/rune claim verifier, and Stage 3U executes only the cookie signed-variant
pack. None of those stages processes raw Discord logs.

## What Not To Commit

Raw Discord HTML, raw message bodies, usernames, user IDs, message IDs, private attachment URLs,
generated extraction outputs, generated promotion outputs, generated redacted shards, or local
review indexes, generated Stage 3R audit JSONL outputs, generated Stage 3S post-Discord
candidate outputs, generated Stage 3T verification outputs, or generated Stage 3U hash outputs.

## Troubleshooting

If the HTML format changes, add a synthetic fixture and adapt the parser without committing raw
chat content. If a redacted shard is too broad for Deep Research, split by topic rather than
uploading raw HTML.

If a Stage 3R lead is Discord-only, keep it quarantined until it has a public source or exact
artefact reference.
