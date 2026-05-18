# Discord Ingestion CLI

Validate the raw-log-free path:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-ingest scan `
  --source-dir third_party/LiberPrimusDiscordChats `
  --out-dir experiments/results/discord-ingestion/stage3n `
  --allow-missing `
  --allow-warnings

.\.venv\Scripts\python.exe -m libreprimus.cli discord-ingest validate-results `
  --results-dir experiments/results/discord-ingestion/stage3n `
  --allow-missing

.\.venv\Scripts\python.exe -m libreprimus.cli discord-ingest summary `
  --results-dir experiments/results/discord-ingestion/stage3n

.\.venv\Scripts\python.exe -m libreprimus.cli discord-ingest export-aggregate `
  --results-dir experiments/results/discord-ingestion/stage3n `
  --archive-out data/locks/third-party/discord-chats/discord-archive-summary-v0.yaml `
  --observation-out data/observations/discord/discord-ingestion-aggregate-summary-v0.yaml `
  --allow-missing
```

The commands do not require raw logs in CI when `--allow-missing` is used. Generated JSONL and
local HTML review files remain ignored.

Stage 3O adds promotion commands for the ignored Stage 3N output:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli discord-promote promote `
  --ingestion-dir experiments/results/discord-ingestion/stage3n `
  --out-dir experiments/results/discord-promotion/stage3o `
  --promoted-links-out data/observations/discord/promoted-public-source-links-stage3o.yaml `
  --promoted-methods-out data/observations/discord/promoted-method-claim-candidates-stage3o.yaml `
  --promoted-numerics-out data/observations/discord/promoted-numeric-observation-candidates-stage3o.yaml `
  --allow-missing `
  --allow-warnings

.\.venv\Scripts\python.exe -m libreprimus.cli discord-promote validate-promoted `
  --links data/observations/discord/promoted-public-source-links-stage3o.yaml `
  --methods data/observations/discord/promoted-method-claim-candidates-stage3o.yaml `
  --numerics data/observations/discord/promoted-numeric-observation-candidates-stage3o.yaml `
  --allow-empty
```

Promotion is redacted, bounded, and review-only.

Stage 3Q adds redacted review-bundle commands:

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

Generated Stage 3Q topic shards and indexes are ignored by default.
