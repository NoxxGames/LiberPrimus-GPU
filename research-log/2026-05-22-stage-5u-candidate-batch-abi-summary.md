# Stage 5U Candidate Batch ABI Summary

Stage 5U defines Candidate Batch ABI v0 as shared contract metadata for future native and CUDA backend work. It closes the Stage 5T shared ABI gaps by contract, not by implementation.

Record counts:

- Candidate batch ABI records: 1.
- Token-buffer contract records: 8.
- Transform-parameter contract records: 6.
- Key-schedule contract records: 2.
- Stream-schedule contract records: 2.
- Score-vector contract records: 7.
- Top-k output contract records: 1.
- Backend-surface contract records: 7.
- Result-store compatibility records: 3.
- ABI gap closure records: 5.
- Next-stage decision records: 9.

The ABI keeps `gematria_shift_score` parity distinct from original transform-family semantics. It does not authorize new kernels, additional CUDA execution, broad solved-fixture expansion, unsolved-page CUDA, benchmarking, or generated-body publication.

Generated reports remain ignored under `experiments/results/cuda-candidate-batch-abi/stage5u/`.
