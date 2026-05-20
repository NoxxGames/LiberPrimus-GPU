# CUDA Kernel Contract CLI

Stage 5E adds the `libreprimus cuda-kernel-contract` command group.

Build the first-kernel contract:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-kernel-contract select-first-kernel `
  --manifest experiments/manifests/cuda/stage5e-first-kernel-contract.yaml `
  --out-dir experiments/results/cuda-kernel-contract/stage5e `
  --allow-warnings
```

Build the native parity adapter map:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-kernel-contract build-native-parity-map `
  --manifest experiments/manifests/cuda/stage5e-adapter-selection.yaml `
  --out-dir experiments/results/cuda-kernel-contract/stage5e `
  --allow-warnings
```

Build readiness and summary:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-kernel-contract build-readiness `
  --manifest experiments/manifests/cuda/stage5e-implementation-readiness.yaml `
  --out-dir experiments/results/cuda-kernel-contract/stage5e `
  --allow-warnings

.\.venv\Scripts\python.exe -m libreprimus.cli cuda-kernel-contract build-summary `
  --out-dir experiments/results/cuda-kernel-contract/stage5e `
  --allow-warnings
```

Validate:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-kernel-contract validate-stage5e `
  --results-dir experiments/results/cuda-kernel-contract/stage5e
```

The CLI is contract-only. It must not execute CUDA transforms, run GPU benchmarks, or write
publishable generated outputs.
