# Archive Visual Registry CLI

Validate source records:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli archive validate-sources --records data/observations/archive/source-archive-records-v0.yaml
```

Scan local page images:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli archive scan-local-images `
  --source-dir third_party/LiberPrimusPages `
  --lock-out data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl `
  --artifact-out data/observations/visual/liber-primus-page-image-artifacts-v0.jsonl `
  --summary-out experiments/results/archive-visual-registry/stage3k/local-image-scan-summary.json `
  --allow-missing
```

Validate image locks:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli archive validate-image-locks `
  --locks data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl `
  --artifacts data/observations/visual/liber-primus-page-image-artifacts-v0.jsonl `
  --allow-empty
```

Validate and summarize observations:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli observation validate-visual --records data/observations/visual/visual-numeric-observations-v0.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli observation validate-cookies --records data/observations/web/cookie-hash-records-v0.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli observation summary `
  --visual data/observations/visual/visual-numeric-observations-v0.yaml `
  --cookies data/observations/web/cookie-hash-records-v0.yaml `
  --sources data/observations/archive/source-archive-records-v0.yaml
```
