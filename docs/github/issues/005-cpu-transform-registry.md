# Implement CPU transform registry and baseline cipher modules

## Summary

Create a CPU-first transform registry for future cipher modules.

## Current Status

Stage 1B adds known-solved fixture reproduction for `reverse_gematria` and `rotated_reverse_gematria`. Direct translation from Stage 1A remains passing.

Vigenere, prime streams, generic affine search, scoring, and full transform registry generalization remain open.

## Scope

Define transform metadata, parameters, CPU reference behavior, and tests for baseline transforms.

## Non-Goals

Do not add GPU kernels before CPU correctness and parity tests exist.

## Deliverables

Registry API, direct translation baseline, Caesar/Atbash scaffolds if policy is ready, and tests.

## Acceptance Criteria

Transforms are manifest-addressable and covered by deterministic tests.

## Safety/Provenance Rules

Do not describe unimplemented transforms as working solver modules.

Suggested labels: stage-1, corpus, testing, safety

## Dependencies

Frozen Gematria profile and canonical corpus candidate.

## Links

- `CIPHER_CATALOG.md`
- `ARCHITECTURE.md`
