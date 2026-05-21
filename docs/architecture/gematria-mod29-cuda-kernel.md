# Gematria Mod-29 CUDA Kernel

Stage 5J adds exactly one scoped CUDA kernel: `gematria_mod29_shift_score_kernel`.

The kernel implements the Stage 5H/5I numeric Gematria shift contract for synthetic parity only:

- token domain: integers `0..28`
- arithmetic: `(token + shift) % 29`
- separator handling: non-transformable token slots are preserved by mask
- output layout: deterministic candidate-major rows
- fixture hash: `a6d5d5161145fd31ab429a8e955e0412d7b0af6089f06ee8b33baf8cd00b27a0`

The Stage 5F uppercase Latin synthetic kernel remains separate and has hash
`76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66`.

Stage 5J does not make production Gematria CUDA ready. It does not run real Liber Primus data,
solved fixtures, unsolved pages, benchmarks, speedup claims, broad experiments, raw-data processing,
website expansion, canonical corpus activation, page-boundary finalisation, or solve claims.
