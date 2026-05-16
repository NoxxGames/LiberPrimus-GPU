# Stage 2A Transform Registry

## Status

Stage 2A is complete when the all-known solved-baseline manifest reproduces 10 known solved fixtures through registry dispatch.

## Stage Goal

Create a CPU reference transform registry and a manifest-addressable solved-baseline runner without enabling search, scoring, CUDA, canonical corpus activation, or page-boundary finalization.

## Inputs

- Stage 0E frozen profiles.
- Stage 1A direct-translation fixtures.
- Stage 1B Atbash-family fixtures.
- Stage 1C explicit-key Vigenere fixtures.
- Stage 1D p56 prime-stream fixture.

## Registry Created

The registry is `data/transform-registry/cpu-reference-transforms-v0.json`. It registers direct translation, reverse Gematria, rotated reverse Gematria, explicit-key Vigenere, prime-minus-one, and the `phi_prime_stream` alias.

## Manifests Created

The solved-baseline manifests live under `experiments/manifests/solved-baselines/`, including the all-known manifest `stage2a-all-known-solved-baselines.yaml`.

## Runner Behaviour

The runner loads the manifest, validates the registry lock and fixture groups, reproduces each fixture group through registry dispatch, and writes ignored records under `experiments/results/solved-baselines/stage2a/`.

## Solved Baseline Result

The Stage 2A smoke result is expected to be 10 passing fixtures, 0 failures, 0 pending, and 0 skipped.

## Regression Coverage

The manifest covers direct translation `4`, Atbash-family `3`, Vigenere `2`, and prime-stream `1`.

## What This Stage Proves

The known solved fixture baselines can be reproduced through a registry and manifest path with stable metadata and disabled search/CUDA/scoring flags.

## What This Stage Does Not Prove

It does not solve new pages, activate the corpus, finalize page boundaries, add scoring, or run any search campaign.

## Next Stage

Stage 2B should add experiment result-store and run-record foundations before unsolved-page search work begins.
