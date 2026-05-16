# Reverse Gematria And Rotated Reverse

## Purpose

This document defines the CPU reference transforms added for Stage 1B solved-fixture reproduction.

## Z_29 Domain

Transforms operate on Gematria profile v0 indices in `Z_29`. The Stage 0E Gematria profile is the source of truth for index, rune, prime, and preferred Latin label lookup.

## Reverse Gematria

```text
decoded_index = 28 - cipher_index
```

Examples:

- `0 -> 28`
- `28 -> 0`
- `14 -> 14`

## Rotated Reverse Gematria

```text
decoded_index = (28 - cipher_index + rotation) mod 29
```

For `rotation=3`:

- `0 -> 2`
- `28 -> 3`
- `2 -> 0`

Rotation is an explicit fixture parameter. Stage 1B does not infer rotations, search rotations, or run brute force.

## Known Solved Fixtures

- `A Warning`: reverse Gematria.
- `A Koan: A Man`: rotated reverse Gematria with `rotation=3`.
- `An Instruction`: rotated reverse Gematria with `rotation=3`, distinct from the Stage 1A direct-translation instruction fixture.

## Non-Goals

This module does not implement Vigenere, prime streams, generic affine search, scoring, CUDA kernels, or unsolved-page search.

## Tests

Stage 1B tests cover formulas, explicit rotation validation, synthetic reproduction, direct-regression reproduction, CLI behavior, and real-source conditional fixture reproduction.

## Future Affine Relationship

Reverse Gematria is affine over `Z_29` with `a=-1, b=28`. Rotated reverse Gematria is affine with `a=-1, b=28+rotation`. Stage 1B documents that relationship but does not implement generic affine search.
