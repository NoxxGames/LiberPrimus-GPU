# Stage 5AA Prime-Minus-One CUDA Synthetic

Stage 5AA is a bounded CUDA correctness stage, not a cryptanalytic experiment.

It adds the synthetic-only `prime_minus_one_stream_kernel_v0` path, runs the single Stage 5Z validation vector when local CUDA is available, records compact metadata under `data/cuda/`, and writes generated reports under ignored `experiments/results/prime-minus-one-cuda-synthetic/stage5aa/`.

Stop conditions:

- Do not run p56/full-p56 CUDA.
- Do not run unsolved pages or broad solved fixtures.
- Do not run scored experiments or benchmarks.
- Do not publish generated result bodies.
- Do not upgrade method status or claim a solve.
