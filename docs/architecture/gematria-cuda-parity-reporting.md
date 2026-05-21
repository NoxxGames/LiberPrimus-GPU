# Gematria CUDA Parity Reporting

Stage 5K turns the Stage 5J synthetic Gematria CUDA/native hash match into durable reporting records. It does not widen CUDA execution.

The reported kernel is `gematria_mod29_shift_score_kernel` under source contract `gematria_mod29_shift_score_contract_v0`. The Stage 5J CUDA output hash and Stage 5H native fixture hash are both `a6d5d5161145fd31ab429a8e955e0412d7b0af6089f06ee8b33baf8cd00b27a0`.

Stage 5K writes:

- `data/cuda/stage5k-gematria-cuda-parity-report.yaml`
- `data/cuda/stage5k-gematria-cuda-device-code-audit.yaml`
- `data/cuda/stage5k-gematria-solved-fixture-safe-preflight.yaml`
- `data/cuda/stage5k-gematria-cuda-score-summary-preflight.yaml`
- `data/cuda/stage5k-gematria-cuda-parity-reporting-summary.yaml`

Generated JSON reports remain ignored under `experiments/results/gematria-cuda-parity-reporting/stage5k/`.

Stage 5K records `new_cuda_kernels_added=0`, `cuda_source_modified=false`, `cuda_execution_performed=false`, `gpu_benchmark_performed=false`, and `performance_claim=false`. Local CUDA paths or GPU memory notes are optional diagnostics only and are not CI requirements.

The device-code audit checks CUDA-facing `.cu` and `.cuh` files for conservative CUDA-C subset drift. It rejects STL containers or strings, exceptions, lambdas, C++ ownership types crossing the kernel boundary, and C++ dynamic allocation tokens in the audited device path.
