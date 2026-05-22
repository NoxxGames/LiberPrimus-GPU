# Prime-Minus-One CUDA Synthetic Kernel

Stage 5AA adds `prime_minus_one_stream_kernel_v0` as a synthetic-only CUDA implementation of the Stage 5Z prime-minus-one stream contract.

Scope:

- Executes only `stage5z-validation-synthetic-prime-control-v0`.
- Input tokens are the committed synthetic control `[0, 2, separator, 2]`.
- Stream values are `(prime_i - 1) mod 29`, using `[1, 2, 4]` for the transformable positions.
- Expected output is `[28, 0, separator, 27]`.
- Expected output-token hash is `06a5c37f7e5eda8eec00cfab5b09faba6ec157488ca15f61a9189d4bf06005ab`.

The kernel preserves separator tokens, uses transformable masks, and keeps p56/full-p56, unsolved pages, scored experiments, benchmarks, and generated-body publication outside the stage scope.
