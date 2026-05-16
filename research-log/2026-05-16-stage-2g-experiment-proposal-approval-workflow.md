# Stage 2G Experiment Proposal Approval Workflow

## Status

Complete pending remote CI verification.

## Goal

Prepare a proposal and explicit human-approval workflow for future bounded exploratory CPU experiments without executing any proposal.

## Inputs

- Stage 2E exploratory dry-run planner.
- Stage 2F synthetic and solved-fixture-only execution harness.
- Existing raw-data-free consistency, CI, result-store, and documentation checks.

## Result

Stage 2G adds proposal schemas, blocked proposal examples, pending/denied approval examples, approval-gate logic, generated review packets, and `libreprimus proposal` CLI commands.

Local validation passed with `418` Python tests, `131` consistency checks, public documentation checks, lock-hash checks, workflow-static checks, and the Stage 2G review smoke. The smoke generated `5` review packets, blocked all `5` proposals, and approved `0`.

## What This Stage Does Not Prove

It does not prove any unsolved-page candidate, execute any proposal, generate candidate plaintexts, score outputs, use CUDA, activate a canonical corpus, or finalize page boundaries.

## Next Stage

Stage 2H should implement an approval-gated execution path, initially limited to synthetic/solved controls or a no-op real proposal.
