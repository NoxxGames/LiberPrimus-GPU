# First CUDA Kernel Contract

Stage 5E selects the first future CUDA kernel contract without adding CUDA implementation. Stage 5F
then implements only that contract as a synthetic CUDA parity target.

Selected contract:

- Kernel id: `shift_score_kernel`
- Target id: `stage5a-caesar_mod29-cuda-target`
- Transform family: `caesar_mod29`
- Adapter family: `native_cpu_synthetic_shift_adapter`
- Readiness: `ready_for_stage5f_synthetic_only_implementation`

The contract is anchored to the Stage 5D native synthetic shift fixture. The one-thread and
multi-thread native output hashes both equal
`76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66`, and Python/native parity
is recorded as true.

This is a contract only stage. It does not add or modify `.cu` or `.cuh` files, run CUDA
transforms, run GPU benchmarks, claim speedups, process raw data, expand the website, activate the
canonical corpus, finalise page boundaries, or make solve claims.

The Stage 5F implementation remains synthetic-only and inherits the same guardrails. It does not
turn the contract into broad CUDA execution or production Gematria mod-29 semantics.

Stage 5G reports the Stage 5F synthetic hash match and records conservative CUDA-C device-code
subset compliance. It does not change the selected contract into solved-fixture-safe or production
Gematria CUDA work.
