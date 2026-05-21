# Gematria Shift CUDA Parity

Stage 5J parity is a synthetic correctness check against the Stage 5H native fixture hash.

Parity passes only when the CUDA output hash equals:

`a6d5d5161145fd31ab429a8e955e0412d7b0af6089f06ee8b33baf8cd00b27a0`

The parity surface is intentionally narrow. It verifies numeric token arithmetic and separator-mask
preservation for the committed validation vector, not production corpus handling. Stage 5K may
report this parity surface and inspect solved-fixture-safe blockers, but solved or unsolved page
CUDA execution remains blocked until a future explicit stage clears source, fixture, scoring, and
benchmark gates.

Generated Stage 5J reports stay under ignored `experiments/results/gematria-cuda-kernel/stage5j/`.
`codex-output/**` handoff files are local and ignored.
