# Stage 5A CUDA Planning Parity Scaffolding

Stage 5A is not an experiment execution stage. It writes planning metadata for future CUDA parity work.

Local run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-planning build-target-plan `
  --manifest experiments/manifests/cuda/stage5a-cuda-target-plan.yaml `
  --out-dir experiments/results/cuda-planning/stage5a `
  --target-plan-out data/cuda/stage5a-cuda-target-plan.yaml `
  --non-targets-out data/cuda/stage5a-cuda-non-targets.yaml `
  --allow-warnings

.\.venv\Scripts\python.exe -m libreprimus.cli cuda-planning build-parity-scaffold `
  --manifest experiments/manifests/cuda/stage5a-cuda-parity-scaffold.yaml `
  --out-dir experiments/results/cuda-planning/stage5a `
  --parity-scaffold-out data/cuda/stage5a-cuda-parity-scaffold.yaml `
  --allow-warnings

.\.venv\Scripts\python.exe -m libreprimus.cli cuda-planning build-implementation-gates `
  --manifest experiments/manifests/cuda/stage5a-cuda-implementation-gates.yaml `
  --out-dir experiments/results/cuda-planning/stage5a `
  --implementation-gates-out data/cuda/stage5a-cuda-implementation-gates.yaml `
  --summary-out data/cuda/stage5a-cuda-planning-summary.yaml `
  --allow-warnings
```

Validation:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-planning validate-stage5a `
  --target-plan data/cuda/stage5a-cuda-target-plan.yaml `
  --parity-scaffold data/cuda/stage5a-cuda-parity-scaffold.yaml `
  --implementation-gates data/cuda/stage5a-cuda-implementation-gates.yaml `
  --non-targets data/cuda/stage5a-cuda-non-targets.yaml `
  --summary data/cuda/stage5a-cuda-planning-summary.yaml `
  --results-dir experiments/results/cuda-planning/stage5a
```

The generated report files under `experiments/results/cuda-planning/stage5a/` are ignored and must not be committed.
