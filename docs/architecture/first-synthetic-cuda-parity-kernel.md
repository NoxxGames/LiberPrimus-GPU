# First Synthetic CUDA Parity Kernel

Stage 5F adds the first real CUDA kernel target in the repository, but only for a raw-data-free
synthetic parity fixture.

The implemented kernel is `shift_score_kernel` for the Stage 5E target
`stage5a-caesar_mod29-cuda-target`. The parity reference is the Stage 5D native synthetic shift
fixture, not production Gematria Primus data.

## Scope

- Fixture text: `LIBER PRIMUS STAGE FIVE D`
- Shifts: `0, 1, 3, 7, 13, 28`
- Character semantics: uppercase Latin A-Z shifted modulo 26
- Non-alpha handling: preserve unchanged
- Reference hash: `76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66`

## Boundaries

Stage 5F does not run real Liber Primus data through CUDA, execute solved or unsolved page
transforms, run GPU benchmarks, make performance or speedup claims, process raw data, publish
generated outputs, activate the canonical corpus, finalise page boundaries, or make solve claims.

No-GPU CI remains valid. Local CUDA builds and synthetic parity runs are optional metadata.
