# Image Transform CLI

Stage 3P adds:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli image-transform run-local-pages `
  --source-dir third_party/LiberPrimusPages `
  --image-locks data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl `
  --out-dir experiments/results/image-transforms/stage3p `
  --allow-missing `
  --allow-warnings
```

Validate generated outputs:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli image-transform validate-results `
  --results-dir experiments/results/image-transforms/stage3p `
  --allow-missing
```

Print the run summary:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli image-transform summary `
  --results-dir experiments/results/image-transforms/stage3p
```

`--allow-missing` keeps CI raw-image-free. The commands do not process Discord logs and do not fetch external resources.
