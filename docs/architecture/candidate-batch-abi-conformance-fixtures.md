# Candidate Batch ABI Conformance Fixtures

Stage 5V conformance fixtures are raw-data-free records that exercise Candidate Batch ABI v0 surfaces without broad experiment execution.

## Fixture Classes

- Executed Python reference fixtures: deterministic `shift_mod29` token-buffer fixtures with output-token hashes.
- Shape-only fixtures: key schedule, stream schedule, score-vector, and top-k records that validate layout and policy without claiming family semantics.
- Blocked/deferred rows: unresolved implementation gaps remain explicit instead of being treated as supported.

## Counts

- Conformance fixture records: `7`
- Executed fixture records: `3`
- Shape-only fixture records: `4`
- Output hash records: `3`

## Policy

The fixtures are not solved-page evidence. They are compatibility and conformance records for future native/CUDA work. They keep `gematria_shift_score_only` parity distinct from direct translation, reverse Gematria, Vigenere, affine, and prime-stream original-family semantics.

Stage 5W uses the conformance records as inputs for prime-minus-one stream contract preparation. It does not reclassify shape-only fixture families as implemented.
