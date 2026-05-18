# Discord Archive Ingestion

## Purpose

Scan admin-provided local Discord HTML exports as source-discovery material only.

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
```

## Expected Outputs

Ingestion writes ignored extraction JSONL and a local review index. Promotion writes capped,
redacted YAML records for public review.

## What Not To Commit

Raw Discord HTML, message bodies, usernames, user IDs, message IDs, private attachment URLs, or
generated extraction/review outputs.

## Troubleshooting

If the HTML format changes, add a synthetic fixture and adapt the parser without committing raw
chat content.
