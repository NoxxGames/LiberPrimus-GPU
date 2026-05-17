# Approval-Gated Execution

## Purpose

Stage 2H proves that proposal approval records can gate execution before any broader exploratory work begins.

## Approval Gate Architecture

The gate binds an `approval_gated_execution_request` to one proposal and one approval record. It loads the Stage 2G proposal, validates the approval record, checks proposal SHA-256, verifies the approval scope, checks expiry, and enforces Stage 2H scope restrictions.

## Request Model

Requests declare the proposal path, approval record path, output directory, execution scope, and false safety flags. Allowed scopes are `synthetic_only`, `solved_fixture_only`, `synthetic_and_solved_fixture_only`, and `no_op_review_only`.

## Approval Record Model

Approved records must be explicit, scoped, non-expired, and constrained. Stage 2H commits approved examples only for synthetic and solved-control proposals.

## Execution Bridge

When the gate passes, the bridge delegates to the Stage 2F CPU execution harness using a declared safe execution manifest. Blocked requests produce blocked plan/result records and do not execute.

## Safe Scopes

Safe execution is limited to synthetic controls and solved-fixture controls. These runs are test controls, not cryptanalysis campaigns.

## Blocked Scopes

Future unsolved page candidates, page candidates that are not solved-fixture-only, and no-op review-only requests remain blocked.

## Result Records

Generated plans and results live under `experiments/results/approval-gated-execution/` and remain ignored by Git.

## Non-goals

Stage 2H does not execute real unsolved pages, generate candidate plaintexts for unsolved material, score outputs, use CUDA, activate canonical corpus, or finalize page boundaries.

## Future Transition

A future stage may prepare a real reviewed approval packet. Execution still requires explicit human approval and a separate stage decision.

