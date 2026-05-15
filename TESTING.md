# Testing

## Test policy

Tests protect reproducibility and prevent false-positive drift.

## Unit tests

Unit tests cover small deterministic functions and placeholder status in Stage 0A.

## Integration tests

Integration tests will later cover manifest execution and result writing.

## Golden tests

Golden tests will later reproduce known solved-page behavior from locked fixtures. None are included in Stage 0A.

## Property tests

Property tests will later check transform invariants, inverse behavior, and edge cases.

## Fuzz tests

Fuzz tests will later target parsers, manifest loading, corpus normalization, and transform composition.

## CPU/GPU parity tests

Every CUDA kernel must match a CPU reference implementation across representative inputs and edge cases.

## Manifest determinism tests

Manifests must replay to the same outputs under pinned inputs and fixed seeds.

## Documentation consistency tests

Documentation checks should verify core policy statements such as raw-data immutability and Stage 0A restrictions.

## Stage 0A smoke tests

Stage 0A includes C++ and Python smoke tests only.
