# CUDA Parity CLI

The `libreprimus cuda-parity` command group manages Stage 5B planning-only CUDA parity harness records.

## Commands

- `build-harness-plan`: builds harness and parity fixture records from Stage 5A target/scaffold records.
- `build-backend-capability`: records CI no-GPU, compatibility 8 GB, and optional local 16 GB backend capability profiles.
- `build-future-kernel-matrix`: records future kernel parity matrix rows as planned or blocked.
- `validate-stage5b`: validates committed Stage 5B records and ignored generated summary consistency.
- `summary`: prints the committed aggregate Stage 5B summary.

These commands do not execute CUDA kernels, run GPU benchmarks, or require CUDA hardware. Generated reports are ignored under `experiments/results/cuda-parity/stage5b/`.
