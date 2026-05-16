# Stage 2D Follow-Up README Boundary Wording

## Status

Complete pending commit, push, and remote README verification.

## Goal

Clarify the public README so readers do not interpret early-stage non-goals as permanent project exclusions.

## Result

The README now distinguishes permanent safety rules, current implementation boundaries, deferred future work, and infrastructure already implemented since Stage 0A. This preserves the no-solve-claim and raw-data safeguards while making clear that CPU experiments, scoring, search, CUDA kernels, and benchmarks are deferred staged work rather than blanket exclusions.

Validation passed locally with Ruff, the full Python test suite, smoke, public documentation checks, lock-hash verification, workflow static validation, documentation consistency, and the full Stage 2D consistency suite.

## What This Does Not Prove

This follow-up does not add search, scoring, CUDA implementation, canonical corpus activation, page-boundary finalization, or any unsolved-page solve claim.

## Next Stage

Stage 2E should design a CPU exploratory experiment manifest scaffold and dry-run planner for bounded baseline transforms without executing unsolved-page search campaigns.
