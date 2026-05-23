# Source Harvester Workflow

Use this workflow when running the Stage 5AF harvester locally.

1. Validate the committed manifest:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester validate-manifest `
  --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml
```

2. Build a dry-run plan:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester plan `
  --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml `
  --out experiments/results/source-harvester/stage5af/harvest_plan.json
```

3. Put user-provided exports/downloads only under ignored local roots:

- `source-harvester-output/`
- `harvest-output/`
- `research-inputs/`
- another ignored local path outside the repo

Do not use Google Drive as storage for this project. For Google Sheet, Google Doc, Google Colab, and Dropbox sources, manually export files to local ignored storage, then inventory those local files.

4. Hash or inventory local material:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester hash-path `
  --path source-harvester-output `
  --out experiments/results/source-harvester/stage5af/local_hashes.jsonl
```

5. Commit only compact metadata when a future prompt explicitly scopes it. Do not commit raw downloads, archives, scraped bodies, images, audio, video, generated bundles, or `codex-output/**`.
