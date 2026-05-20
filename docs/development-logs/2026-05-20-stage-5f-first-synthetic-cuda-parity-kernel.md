# Stage 5F - First Synthetic CUDA Parity Kernel

Date: 2026-05-20

## Scope

Stage 5F implemented only the Stage 5E selected `shift_score_kernel` CUDA contract for the Stage 5D
synthetic uppercase-shift fixture. The stage kept no-GPU CI compatibility and recorded optional local
CUDA build/parity metadata.

## Work Completed

- Added `cuda/include/libreprimus/shift_score_kernel.cuh` and `cuda/kernels/shift_score_kernel.cu`.
- Added CMake and CTest wiring for `lpgpu_cuda_shift_score_test`.
- Added `libreprimus cuda-kernel` commands for implementation, build, parity, summary, and validation records.
- Added Stage 5F schemas, manifests, committed YAML summaries, tests, docs, tutorials, and research-synthesis records.
- Generated reports under `experiments/results/cuda-kernel/stage5f/`, which remain ignored.

## Guardrails

No real Liber Primus data, solved pages, unsolved pages, GPU benchmarks, speedup claims, broad
experiments, raw data processing, generated-output publication, website expansion, canonical corpus
activation, page-boundary finalisation, or solve claims were added.
