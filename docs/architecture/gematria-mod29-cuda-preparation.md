# Gematria Mod-29 CUDA Preparation

Stage 5I turns the Stage 5H Gematria mod-29 `shift_score` contract into a future implementation
package. It is preparation only: no CUDA source is added, no CUDA transform is executed, and no
real Liber Primus data is used.

Stage 5J consumes this preparation package for the scoped synthetic numeric
`gematria_mod29_shift_score_kernel`. Stage 5I remains the ABI/vector source of truth; Stage 5J is
hash-matching synthetic implementation metadata, not production Gematria CUDA readiness.
Stage 5K records the Stage 5J hash match and solved-fixture-safe blockers without executing CUDA.

## Contract

- Source contract: `gematria_mod29_shift_score_contract_v0`
- Future kernel: `gematria_mod29_shift_score_kernel`
- Token domain: integer values `0..28`
- Arithmetic: `(token + shift) % 29`
- Separator policy: separators remain unshifted through `transformable_mask=0`
- Validation fixture hash: `a6d5d5161145fd31ab429a8e955e0412d7b0af6089f06ee8b33baf8cd00b27a0`

## Stage 5J Boundary

Stage 5J may implement only the synthetic numeric parity path described by Stage 5I. It must keep
the Stage 5F uppercase Latin synthetic kernel separate, compare CUDA token-output hashes against the
Stage 5H native fixture hash, and preserve no-GPU-safe CI validation.

Solved fixtures, unsolved pages, real Liber Primus CUDA data, GPU benchmarks, speedup assertions,
website expansion, canonical corpus activation, page-boundary finalisation, and solve claims remain
blocked.

## Stage 5K Boundary

Stage 5K may report the Stage 5J parity surface and build solved-fixture-safe preflight records
only. It adds no kernels, changes no CUDA source, executes no CUDA, and leaves production Gematria
CUDA blocked pending token mapping, score-summary parity, no-unsolved guardrails, and future-stage
approval.
