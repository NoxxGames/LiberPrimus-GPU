# Discord Review Bundle CLI

Stage 3Q CLI group:

```text
libreprimus discord-review
```

## Build Bundles

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

`--allow-missing` keeps CI raw-log-free. With real Stage 3N outputs present, the command writes redacted review bundles to ignored output paths and writes an aggregate YAML summary.

## Validate Bundles

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-review validate-bundles `
  --results-dir experiments/results/discord-review-bundles/stage3q `
  --aggregate data/observations/discord/discord-review-bundle-aggregate-stage3q.yaml `
  --allow-missing
```

Validation checks privacy flags, generated output presence, aggregate safety, and missing-input mode.

## Summary

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-review summary `
  --results-dir experiments/results/discord-review-bundles/stage3q `
  --aggregate data/observations/discord/discord-review-bundle-aggregate-stage3q.yaml
```

The summary prints counts and generated output paths only.

## Output Policy

Do not commit:

- `redacted_message_stream.jsonl`
- `topic_shards/*.md`
- generated JSONL indexes
- `review_index.html`
- raw Discord HTML logs

Only the aggregate YAML, schemas, code, docs, tests, and research logs are committed.
