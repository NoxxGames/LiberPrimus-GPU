# Stage 5B CUDA Parity Harness Skeleton

Stage 5B is not an experiment. It builds metadata and validation surfaces for future CUDA parity work.

Run validation:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-parity validate-stage5b `
  --harness-plan data/cuda/stage5b-cuda-parity-harness-plan.yaml `
  --parity-fixtures data/cuda/stage5b-cuda-parity-fixtures.yaml `
  --backend-capability data/cuda/stage5b-cuda-backend-capability.yaml `
  --future-kernel-matrix data/cuda/stage5b-future-kernel-parity-matrix.yaml `
  --summary data/cuda/stage5b-cuda-parity-harness-summary.yaml `
  --results-dir experiments/results/cuda-parity/stage5b
```

The build commands may create ignored JSON reports under `experiments/results/cuda-parity/stage5b/`. Those files are diagnostics only and must not be committed.

Stage 5B keeps every future kernel as `planned` or `blocked`; no implemented kernel row is allowed.
