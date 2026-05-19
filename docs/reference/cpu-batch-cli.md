# CPU Batch CLI

Stage 4H adds:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cpu-batch validate-manifest `
  --manifest experiments/manifests/cpu-batch/stage4h-synthetic-smoke-batch.yaml
```

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cpu-batch run `
  --manifest experiments/manifests/cpu-batch/stage4h-synthetic-smoke-batch.yaml `
  --out-dir experiments/results/cpu-batch/stage4h `
  --allow-warnings
```

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cpu-batch adapter-coverage `
  --registry data/transform-registry/cpu-reference-transforms-v0.json `
  --out-dir experiments/results/cpu-batch/stage4h `
  --allow-warnings
```

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cpu-batch validate-results `
  --results-dir experiments/results/cpu-batch/stage4h
```

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cpu-batch summary `
  --results-dir experiments/results/cpu-batch/stage4h
```

The CLI is CPU-only. It does not run CUDA, broad search, raw data processing, or solve-claim workflows.
