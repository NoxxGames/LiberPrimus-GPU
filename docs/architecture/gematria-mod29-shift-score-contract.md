# Gematria Mod-29 Shift Score Contract

Stage 5H defines the future production `shift_score_kernel` token contract for Gematria Primus data.
It does not change the Stage 5F CUDA kernel, which remains limited to the uppercase Latin synthetic
fixture.

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
records, Stage 4O parity expectations, and Stage 4I score-summary semantics.
