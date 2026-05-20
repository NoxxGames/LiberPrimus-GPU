# CPU Batch Adapter CLI

Stage 4O extends `libreprimus cpu-batch` with CPU-only adapter expansion commands.

## Solved-Fixture Parity

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cpu-batch solved-fixture-parity `
  --manifest experiments/manifests/cpu-batch/stage4o-solved-fixture-parity-batch.yaml `
  --out-dir experiments/results/cpu-batch/stage4o `
  --allow-warnings
```

## Adapter Expansion

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cpu-batch adapter-expansion `
  --manifest experiments/manifests/cpu-batch/stage4o-adapter-expansion-smoke-batch.yaml `
  --registry data/transform-registry/cpu-reference-transforms-v0.json `
  --out-dir experiments/results/cpu-batch/stage4o `
  --allow-warnings
```

## Parity Readiness

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cpu-batch parity-readiness `
  --manifest experiments/manifests/cpu-batch/stage4o-cpu-cuda-parity-readiness.yaml `
  --out-dir experiments/results/cpu-batch/stage4o `
  --allow-warnings
```

## Validate

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cpu-batch validate-stage4o `
  --results-dir experiments/results/cpu-batch/stage4o `
  --summary data/research/stage4o-cpu-batch-adapter-expansion-summary.yaml
```

These commands do not implement CUDA, run broad experiments, or process raw data.
