# Implement CPU transform registry and baseline cipher modules

## Summary

Create a CPU-first transform registry for future cipher modules.

## Current Status

Stage 2A adds the CPU reference transform registry and manifest-addressable solved-baseline runner. Direct translation, reverse Gematria, rotated reverse Gematria, explicit-key Vigenere, and prime-minus-one known solved baselines reproduce through registry dispatch.

Generic affine/shift search, scoring, CUDA parity, and broader experiment-result storage remain open.

## Scope

Define transform metadata, parameters, CPU reference behavior, and tests for baseline transforms.

## Non-Goals

Do not add GPU kernels before CPU correctness and parity tests exist.

## Deliverables

Registry API, solved-baseline CPU reference transforms, manifest-addressable runner, and tests.

## Acceptance Criteria

Known solved baseline transforms are manifest-addressable and covered by deterministic tests.

## Safety/Provenance Rules

Do not describe unimplemented transforms as working solver modules.

Suggested labels: stage-2, ciphers, testing, needs-human-review

## Dependencies

Frozen Gematria profile and canonical corpus candidate.

## Links

- `CIPHER_CATALOG.md`
- `ARCHITECTURE.md`
