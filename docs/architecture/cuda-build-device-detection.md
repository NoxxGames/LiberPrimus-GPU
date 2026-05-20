# CUDA Build And Device Detection

Stage 5C records CUDA build and device readiness metadata only. It does not add CUDA kernels, run cryptanalytic CUDA work, run GPU benchmarks, claim speedups, expand the website, or make solve claims.

## Boundaries

- `LPGPU_ENABLE_CUDA` remains optional.
- No-GPU CI remains a first-class profile.
- The local 16 GB GPU profile is optional metadata, not a requirement.
- Compatibility 8 GB metadata remains present for future planning.
- Smoke-build records describe configure/build readiness only; they are not parity evidence.

## Records

Committed Stage 5C data lives under `data/cuda/`:

- `stage5c-cuda-build-profiles.yaml`
- `stage5c-cuda-toolchain-detection.yaml`
- `stage5c-cuda-device-detection.yaml`
- `stage5c-cuda-smoke-build-records.yaml`
- `stage5c-cuda-build-device-summary.yaml`

Generated reports remain ignored under `experiments/results/cuda-build/stage5c/`.

## Next Dependency

Future CUDA implementation still needs CPU reference behavior, Stage 5B harness records, Stage 5C build/device records, Stage 5D native CPU output hashes and deterministic threading records, Stage 5E first-kernel contract records, explicit parity tests, and benchmark planning. Stage 5F may implement only the selected synthetic-only contract before any broad CUDA implementation.
