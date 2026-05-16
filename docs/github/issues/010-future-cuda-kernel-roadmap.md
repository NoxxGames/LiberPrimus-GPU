# Plan CUDA kernel roadmap after CPU parity tests

## Summary

Plan CUDA acceleration only after CPU reference transforms and parity tests are available.

## Current Status

CUDA smoke scaffolding exists; no cryptanalysis kernels are implemented.

## Scope

Identify candidate batch transform/scoring kernels, parity requirements, benchmarks, and hardware metadata.

## Non-Goals

Do not implement CUDA kernels in this planning issue.

## Deliverables

Roadmap document, benchmark policy updates, and dependency list.

## Acceptance Criteria

CUDA work is blocked on CPU correctness, parity tests, and benchmark methodology.

## Safety/Provenance Rules

Performance work must not weaken provenance, raw preservation, or correctness.

Suggested labels: cuda, performance, blocked, safety

## Dependencies

CPU transform registry, corpus candidate, and scoring baseline.

## Links

- `CUDA_NOTES.md`
- `BENCHMARKS.md`
