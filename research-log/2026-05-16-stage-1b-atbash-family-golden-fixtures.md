# Stage 1B Atbash-Family Golden Fixtures Research Log

## Summary

Stage 1B reproduced known solved reverse Gematria / Atbash-family sections from locked sources using Stage 0E profiles and Stage 1A fixture infrastructure.

## Evidence

- `A Warning` is documented in the locked scream314 reference as reversed Gematria.
- The 06-09 family containing `A Koan: A Man` and the related `An Instruction` is documented as shift 3 down reversed Gematria.
- Fixture spans are explicit Stage 0E logical-line ranges from the generated rtkd corpus candidate.

## Results

- `A Warning`: pass with `reverse_gematria`.
- `A Koan: A Man`: pass with `rotated_reverse_gematria`, `rotation=3`.
- `An Instruction`: pass with `rotated_reverse_gematria`, `rotation=3`.
- Stage 1A direct fixtures remained passing.

## Interpretation

These are known-solved baseline reproductions only. They do not prove a new page solution, activate a canonical corpus, or finalize page boundaries.

## Remaining Work

Vigenere solved-page reproduction, prime-stream solved-page reproduction, and any future affine/search infrastructure remain separate stages.

## GitHub Tracking

GitHub issue `#5` was updated with Stage 1B results and left open because not all baseline transform families are implemented.
