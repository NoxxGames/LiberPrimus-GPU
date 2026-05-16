# Stage 1B Atbash-Family Golden Fixtures

## Status

Stage 1B is a known-solved reproduction stage. It adds CPU-only reverse Gematria and rotated reverse Gematria reproduction for locked fixture spans. It does not solve unsolved pages, search rotations, activate a canonical corpus, finalize page boundaries, or use CUDA.

## Stage Goal

The goal is to extend the Stage 1A solved-fixture framework beyond direct translation with two explicit Z_29 transforms:

- `reverse_gematria`: `decoded_index = 28 - cipher_index`
- `rotated_reverse_gematria`: `decoded_index = (28 - cipher_index + rotation) mod 29`

## Inputs

- Stage 0E Gematria profile v0: `93577209028c964523068b5975180e05bda5b1a07b2675d4e35d03d6d164c5c2`
- Stage 0E separator grammar v0: `303f3062ad8b41bf84ab068f2fd6601b1efb3291872d53956669ea3dd7d88e3c`
- Stage 0E glyph-variant profile v0: `5acae61c4ea2aa9f2f2fb76bdcafb7ed9c6504bd98caf29590a95d7d43271d6d`
- rtkd master transcript SHA-256: `e21743ccd9a07f3845d52a329c61b9fa69e9ca6a44ee3ba0db8f28a0d7065004`
- scream314 reference SHA-256: `0f7545d470f2056b45b5de2c8c116ecdea66969fdca6be57ccbd8e591e40ee92`

## Scope

Stage 1B fixtures:

- `a-warning-reverse-gematria`
- `a-koan-a-man-rotated-reverse-gematria`
- `an-instruction-rotated-reverse-gematria`

The two rotated fixtures declare `rotation=3` explicitly from the locked reference note that the 06-09 family uses shift 3 down reversed Gematria. No rotation discovery or brute-force pass is implemented.

## Out Of Scope

This stage does not implement Vigenere, prime streams, affine search, scoring, CUDA kernels, or any unsolved-page search. Direct-translation fixtures are run only as regressions.

## Fixture Provenance

Fixture manifests live in `data/fixtures/solved-pages/atbash-family-v0/`. Each fixture includes source transcript SHA-256, solved-reference SHA-256, profile SHA-256s, corpus candidate ID, fixture version, span selector, expected normalized text hash, and canonical false flags.

## Normalized Plaintext Policy

The Stage 1A normalized plaintext policy is reused: Gematria preferred Latin labels are uppercase, word separators become spaces, clause separators become `. `, line separators join wrapped lines, numeric literals are preserved, repeated whitespace collapses, and leading/trailing whitespace is trimmed.

Profile labels are deliberate. For example, the profile preferred label is `C`, so known text conventionally written with K appears with `C` in the normalized fixture expectation.

## Fixture Results

Real-source Stage 1B smoke reproduced:

- Direct regression: `4` pass, `0` fail, `0` pending, `0` skipped.
- Atbash-family: `3` pass, `0` fail, `0` pending, `0` skipped.

Generated outputs are under `data/normalized/solved-baselines/atbash-family-v0/` and remain ignored.

## What This Stage Proves

The current profile and corpus-candidate views can reproduce selected known-solved reverse Gematria and rotated reverse Gematria sections with explicit parameters.

## What This Stage Does Not Prove

Passing fixtures do not activate a canonical corpus, finalize page boundaries, validate unsolved pages, or prove any new solution.

## Next Stage

Recommended next stage: Stage 1C, explicit-key Vigenere solved-page reproduction for locked, documented keys only.
