# Image Analysis CLI

Stage 3M adds the `libreprimus image-analysis` command group.

Analyze local page images:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli image-analysis analyze-local-pages `
  --source-dir third_party/LiberPrimusPages `
  --image-locks data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl `
  --out-dir experiments/results/image-analysis/stage3m `
  --allow-missing `
  --allow-warnings
```

Validate generated results:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli image-analysis validate-results `
  --results-dir experiments/results/image-analysis/stage3m `
  --allow-missing
```

Print a concise summary:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli image-analysis summary `
  --results-dir experiments/results/image-analysis/stage3m
```

`--allow-missing` keeps CI raw-image-free. The commands do not perform OCR, AI/ML interpretation, steganography extraction, image-derived cipher execution, or solve claims.
