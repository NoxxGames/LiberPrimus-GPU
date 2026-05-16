# Add GitHub Actions CI for Python and CMake smoke tests

## Summary

Add CI for Python tests and CMake smoke builds.

## Current Status

Local Python tests pass; CMake smoke scaffolding exists from Stage 0A.

## Scope

GitHub Actions workflow for Python 3.12, ruff, pytest, and CPU-only CMake smoke where feasible.

## Non-Goals

Do not require CUDA in default CI.

## Deliverables

Workflow files, docs, and CI status expectations.

## Acceptance Criteria

CI runs without raw data and passes on clean checkout.

## Safety/Provenance Rules

CI must not download unrelated corpus data or print secrets.

Suggested labels: github, testing, good-first-issue, safety

## Dependencies

Repository public workflow setup.

## Links

- `TESTING.md`
- `scripts/README.md`
