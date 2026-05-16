# Stage 2A CPU Transform Registry Research Log

## Status

Stage 2A consolidates known solved-baseline reproduction behind a CPU reference transform registry and manifest runner.

## Goal

Run all current known solved fixtures through stable registry metadata and a solved-baseline manifest path before adding experiment result storage or search scaffolding.

## Inputs

- Stage 0E Gematria, separator, and glyph-variant profiles.
- Stage 1A direct-translation fixtures.
- Stage 1B reverse Gematria / Atbash-family fixtures.
- Stage 1C explicit-key Vigenere fixtures.
- Stage 1D p56 prime-minus-one fixture.

## Registry

The Stage 2A registry is `cpu-reference-transforms-v0`. It is CPU-only and locked by SHA-256. It registers direct translation, reverse Gematria, rotated reverse Gematria, explicit-key Vigenere, prime-minus-one, and the `phi_prime_stream` alias.

## Manifest Runner

The all-known manifest runs four fixture groups and expects 10 passes. Generated records include manifest and registry hashes plus `search_performed=false`, `cuda_used=false`, and `scoring_used=false`.

## Result

The Stage 2A smoke reproduces all 10 known solved fixture baselines through registry dispatch. No new plaintext is claimed and no unsolved-page search is performed.

## Limits

The registry is not a generic transform search engine. It does not implement scoring, CUDA, affine/shift search, key search, stream offset search, canonical corpus activation, or page-boundary finalization.

## Next

Stage 2B should add experiment result-store and run-record foundations before any unsolved-page search campaign.
