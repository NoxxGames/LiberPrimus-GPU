# CUDA Host Runtime Boundary

The Stage 5C host boundary is detection and build readiness, not CUDA execution. Stage 5D native CPU backend records are separate CPU parity infrastructure and do not authorize CUDA execution.

## Allowed

- Detect CMake, `nvcc`, and `nvidia-smi` availability.
- Record local CUDA device metadata when visible.
- Record no-GPU CI, compatibility 8 GB, and optional local 16 GB profiles.
- Optionally attempt to configure/build the existing CUDA smoke target and record the outcome.

## Prohibited

- Adding or modifying CUDA kernels.
- Running CUDA smoke tests as proof of parity.
- Running GPU benchmarks or claiming speedups.
- Processing raw Discord logs, raw page images, or stego/audio artefacts.
- Expanding website output or publishing generated reports.

Local device records are environment metadata. They cannot be used as solve evidence, performance evidence, or implementation approval.
