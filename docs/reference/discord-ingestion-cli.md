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
