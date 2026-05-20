# CUDA Build Device CLI

Stage 5C adds the `libreprimus cuda-build` command group.

## Profile Toolchain

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-build profile-toolchain `
  --manifest experiments/manifests/cuda/stage5c-cuda-build-device-detection.yaml `
  --out-dir experiments/results/cuda-build/stage5c `
  --profiles-out data/cuda/stage5c-cuda-build-profiles.yaml `
  --toolchain-out data/cuda/stage5c-cuda-toolchain-detection.yaml `
  --allow-missing-cuda `
  --allow-warnings
```

## Detect Device

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-build detect-device `
  --manifest experiments/manifests/cuda/stage5c-cuda-build-device-detection.yaml `
  --out-dir experiments/results/cuda-build/stage5c `
  --devices-out data/cuda/stage5c-cuda-device-detection.yaml `
  --allow-no-gpu `
  --allow-warnings
```

## Smoke Build

The default command records a skipped smoke build. `--attempt-build` is optional and local-only.

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-build smoke-build `
  --manifest experiments/manifests/cuda/stage5c-cuda-no-gpu-ci-profile.yaml `
  --out-dir experiments/results/cuda-build/stage5c `
  --smoke-build-out data/cuda/stage5c-cuda-smoke-build-records.yaml `
  --allow-missing-cuda `
  --allow-no-gpu `
  --allow-warnings
```

## Validate

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-build validate-stage5c `
  --profiles data/cuda/stage5c-cuda-build-profiles.yaml `
  --toolchain data/cuda/stage5c-cuda-toolchain-detection.yaml `
  --devices data/cuda/stage5c-cuda-device-detection.yaml `
  --smoke-build data/cuda/stage5c-cuda-smoke-build-records.yaml `
  --summary data/cuda/stage5c-cuda-build-device-summary.yaml `
  --results-dir experiments/results/cuda-build/stage5c
```
