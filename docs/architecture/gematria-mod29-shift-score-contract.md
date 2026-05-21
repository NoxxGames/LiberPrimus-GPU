# Gematria Mod-29 Shift Score Contract

Stage 5H defines the future production `shift_score_kernel` token contract for Gematria Primus data.
It does not change the Stage 5F CUDA kernel, which remains limited to the uppercase Latin synthetic
fixture.

Stage 5J implements the synthetic CUDA side of this contract only. The matching Stage 5H/5J fixture
hash is `a6d5d5161145fd31ab429a8e955e0412d7b0af6089f06ee8b33baf8cd00b27a0`.
Stage 5K reports that hash match and records solved-fixture-safe blockers without CUDA execution.

## Contract

- Contract id: `gematria_mod29_shift_score_contract_v0`
- Future kernel id: `shift_score_kernel`
- Token domain: integer rune tokens `0..28`
- Arithmetic direction: `forward_add_shift_mod29`
- Formula: `(token + shift) % 29`
- Output ordering: candidate-index order
- Separator policy: preserve non-transformable separators unshifted

Transformable tokens are rune tokens only. Word, clause, paragraph, segment, chapter, page-marker,
whitespace, and unknown-symbol tokens are not shifted.

## Boundary

The Stage 5H contract is metadata and fixture preparation only. It adds no CUDA kernels, performs no
CUDA execution, uses no real Liber Primus page data, runs no solved or unsolved page CUDA transforms,
runs no GPU benchmark, and makes no solve claim.

## Required Future Gates

Future Gematria CUDA work must cite this contract, the Stage 5H native fixture hash, Stage 5G
device-code subset audit records, Stage 5F synthetic parity records, Stage 5D native CPU parity
records, Stage 5I ABI and validation-vector records, Stage 4O parity expectations, and Stage 4I
score-summary semantics. Stage 5J must compare CUDA token-output hashes against the Stage 5H native
fixture hash before any wider use. Stage 5K parity-reporting records must remain blocked for
solved-fixture CUDA until token mapping, score-summary parity, no-unsolved guardrails, and explicit
future-stage approval exist.
