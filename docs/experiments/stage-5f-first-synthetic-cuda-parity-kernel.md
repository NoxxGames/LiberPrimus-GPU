# Stage 5F First Synthetic CUDA Parity Kernel

Stage 5F implemented the selected `shift_score_kernel` target as a synthetic-only CUDA parity
kernel. It added CMake wiring, a host wrapper, a C++/CUDA test, Python metadata builders, schemas,
and the `libreprimus cuda-kernel` CLI.

The stage writes compact committed records under `data/cuda/` and generated ignored reports under
`experiments/results/cuda-kernel/stage5f/`.

## Results

- Implementation records: 1
- Build records: 1
- Synthetic parity records: 1
- Local optional CUDA build status: passed
- Local optional synthetic parity status: passed
- CUDA/native hash match: true

Stage 5F is correctness infrastructure only. It is not a benchmark, speedup claim, broad CUDA
implementation, real Liber Primus CUDA execution, or solve claim.
