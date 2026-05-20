# Gematria CUDA Prep CLI

Stage 5I adds the `libreprimus gematria-cuda-prep` command group.

## Build

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-prep build-kernel-preparation `
  --manifest experiments/manifests/cuda/stage5i-gematria-cuda-kernel-preparation.yaml `
  --out-dir experiments/results/gematria-cuda-prep/stage5i `
  --preparation-out data/cuda/stage5i-gematria-cuda-kernel-preparation.yaml `
  --allow-warnings
```

The remaining build commands are `build-abi-plan`, `build-validation-vectors`,
`build-implementation-checklist`, and `build-summary`.

## Validate

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-prep validate-stage5i `
  --preparation data/cuda/stage5i-gematria-cuda-kernel-preparation.yaml `
  --abi-plan data/cuda/stage5i-gematria-cuda-abi-plan.yaml `
  --validation-vectors data/cuda/stage5i-gematria-cuda-validation-vectors.yaml `
  --implementation-checklist data/cuda/stage5i-gematria-cuda-implementation-checklist.yaml `
  --summary data/cuda/stage5i-gematria-cuda-preparation-summary.yaml `
  --results-dir experiments/results/gematria-cuda-prep/stage5i
```

## Summary

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-prep summary `
  --summary data/cuda/stage5i-gematria-cuda-preparation-summary.yaml
```

The CLI is raw-data-free and no-GPU-safe. Generated reports remain ignored.
