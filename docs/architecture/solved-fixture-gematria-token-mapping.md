# Solved-Fixture Gematria Token Mapping

Stage 5L maps committed solved-fixture-safe Stage 4O input streams into the numeric Gematria token
domain required by the future `gematria_mod29_shift_score_kernel`.

The durable token contract is:

- token domain: integers `0..28`
- arithmetic: `(token + shift) % 29`
- ordering: candidate-major
- transformable entries: rune tokens only
- non-transformable entries: preserved by token kind and transformable mask
- output hash: SHA-256 over canonical JSON hash material

The mapping records are not CUDA execution permission. They prove that the future parity harness has
source-backed numeric buffers and separator metadata for five committed solved-fixture-safe streams.

Stage 5L closed non-execution blockers for token-domain mapping, host-side record shape,
output-token hash definition, Stage 4O linkage, no-unsolved guardrail recheck, and score-summary
shape. The remaining blocker is explicit future-stage approval before solved-fixture-safe CUDA
parity can run.
