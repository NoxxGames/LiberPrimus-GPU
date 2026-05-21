# Gematria Solved-Fixture CUDA CLI

The `libreprimus gematria-solved-fixture-cuda` CLI manages Stage 5M solved-fixture-safe CUDA parity records.

Build pending run records:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-cuda build-run-records `
  --run-records-out data/cuda/stage5m-gematria-solved-fixture-cuda-run.yaml `
  --out-dir experiments/results/gematria-solved-fixture-cuda/stage5m `
  --allow-warnings
```

Run local optional CUDA parity:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-cuda run-cuda-parity `
  --run-records data/cuda/stage5m-gematria-solved-fixture-cuda-run.yaml `
  --run-records-out data/cuda/stage5m-gematria-solved-fixture-cuda-run.yaml `
  --out-dir experiments/results/gematria-solved-fixture-cuda/stage5m `
  --allow-warnings
```

CI-safe no-GPU path:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-cuda run-cuda-parity `
  --run-records stage5m-run.yaml `
  --run-records-out stage5m-run.yaml `
  --out-dir temp/stage5m `
  --skip-run `
  --allow-warnings
```

Build derived records:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-cuda build-parity-records
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-cuda build-boundary-records
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-cuda build-summary
```

Validate committed records:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-cuda validate-stage5m `
  --run-records data/cuda/stage5m-gematria-solved-fixture-cuda-run.yaml `
  --parity-records data/cuda/stage5m-gematria-solved-fixture-cuda-parity.yaml `
  --boundaries data/cuda/stage5m-gematria-solved-fixture-cuda-boundaries.yaml `
  --summary data/cuda/stage5m-solved-fixture-cuda-parity-summary.yaml `
  --results-dir experiments/results/gematria-solved-fixture-cuda/stage5m
```

The CLI must not be used to run unsolved-page CUDA data, raw page text, benchmarks, or broad transform campaigns.
