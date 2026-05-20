# cuda-parity-reporting CLI

Stage 5G adds the raw-data-free, no-GPU-safe CLI group:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-parity-reporting --help
```

## Build Parity Report

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-parity-reporting build-parity-report `
  --manifest experiments/manifests/cuda/stage5g-shift-score-parity-reporting.yaml `
  --out-dir experiments/results/cuda-parity-reporting/stage5g `
  --parity-report-out data/cuda/stage5g-shift-score-parity-report.yaml `
  --allow-warnings
```

## Audit CUDA Device-Code Subset

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-parity-reporting audit-device-code-subset `
  --manifest experiments/manifests/cuda/stage5g-device-code-subset-audit.yaml `
  --out-dir experiments/results/cuda-parity-reporting/stage5g `
  --device-code-audit-out data/cuda/stage5g-cuda-device-code-subset-audit.yaml `
  --allow-warnings
```

## Build Solved-Fixture Preflight

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-parity-reporting build-solved-fixture-preflight `
  --manifest experiments/manifests/cuda/stage5g-solved-fixture-safe-adapter-preflight.yaml `
  --out-dir experiments/results/cuda-parity-reporting/stage5g `
  --preflight-out data/cuda/stage5g-solved-fixture-safe-adapter-preflight.yaml `
  --allow-warnings
```

## Build And Validate Summary

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-parity-reporting build-summary `
  --parity-report data/cuda/stage5g-shift-score-parity-report.yaml `
  --device-code-audit data/cuda/stage5g-cuda-device-code-subset-audit.yaml `
  --preflight data/cuda/stage5g-solved-fixture-safe-adapter-preflight.yaml `
  --summary-out data/cuda/stage5g-cuda-parity-reporting-summary.yaml `
  --out-dir experiments/results/cuda-parity-reporting/stage5g `
  --allow-warnings

.\.venv\Scripts\python.exe -m libreprimus.cli cuda-parity-reporting validate-stage5g `
  --parity-report data/cuda/stage5g-shift-score-parity-report.yaml `
  --device-code-audit data/cuda/stage5g-cuda-device-code-subset-audit.yaml `
  --preflight data/cuda/stage5g-solved-fixture-safe-adapter-preflight.yaml `
  --summary data/cuda/stage5g-cuda-parity-reporting-summary.yaml `
  --results-dir experiments/results/cuda-parity-reporting/stage5g
```

The commands do not require CUDA hardware and do not read raw Liber Primus data.
