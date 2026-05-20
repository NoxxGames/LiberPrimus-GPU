# CUDA Kernel CLI

Stage 5F adds the `libreprimus cuda-kernel` command group.

## Commands

Build implementation records:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-kernel build-implementation-records --manifest experiments/manifests/cuda/stage5f-shift-score-synthetic-parity.yaml --out-dir experiments/results/cuda-kernel/stage5f --implementation-out data/cuda/stage5f-cuda-synthetic-kernel-implementation.yaml --allow-warnings
```

Record a no-GPU-safe skipped build:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-kernel attempt-build --manifest experiments/manifests/cuda/stage5f-cuda-no-gpu-ci-skip.yaml --out-dir experiments/results/cuda-kernel/stage5f --build-records-out data/cuda/stage5f-cuda-kernel-build-records.yaml --skip-build --allow-warnings
```

Attempt optional local CUDA build:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-kernel attempt-build --manifest experiments/manifests/cuda/stage5f-cuda-local-optional-run.yaml --out-dir experiments/results/cuda-kernel/stage5f --build-records-out data/cuda/stage5f-cuda-kernel-build-records.yaml --allow-warnings
```

Run synthetic parity if the optional build passed:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-kernel run-synthetic-parity --manifest experiments/manifests/cuda/stage5f-shift-score-synthetic-parity.yaml --build-records data/cuda/stage5f-cuda-kernel-build-records.yaml --out-dir experiments/results/cuda-kernel/stage5f --parity-records-out data/cuda/stage5f-cuda-synthetic-parity-records.yaml --allow-warnings
```

Validate:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-kernel validate-stage5f --implementation data/cuda/stage5f-cuda-synthetic-kernel-implementation.yaml --build-records data/cuda/stage5f-cuda-kernel-build-records.yaml --parity-records data/cuda/stage5f-cuda-synthetic-parity-records.yaml --summary data/cuda/stage5f-cuda-synthetic-kernel-summary.yaml --results-dir experiments/results/cuda-kernel/stage5f
```

The CLI does not benchmark, run broad experiments, or process raw data.
