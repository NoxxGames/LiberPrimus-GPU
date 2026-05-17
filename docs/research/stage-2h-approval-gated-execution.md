# Stage 2H Approval-Gated Execution

## Stage Goal

Prove that approved synthetic and solved-control proposals can execute through an explicit approval gate while real unsolved proposals remain blocked.

## Inputs

Stage 2H builds on Stage 2G proposal records and Stage 2F safe CPU execution manifests.

## Schemas

The stage adds request, plan, and result schemas for approval-gated execution records.

## Proposals And Approvals

Committed approved approval records exist only for synthetic direct and solved-fixture replay controls. The no-op real proposal uses a pending approval record and remains blocked.

## Execution Path

Passing requests delegate to the Stage 2F CPU execution harness. Blocked requests produce blocked results without execution.

## Safety Gates

The gate checks proposal SHA-256, approval status, `approved_for_execution`, approver, timestamp, scope, constraints, expiry, safe corpus slice, and false search/scoring/CUDA flags.

## Validation Result

Local tests and consistency checks verify safe control execution and blocked real-proposal behavior.

## What This Stage Proves

The approval mechanism can allow approved safe controls and block no-approval, pending, denied, expired, mismatched, wrong-scope, and future-unsolved requests.

## What This Stage Does Not Prove

It does not solve an unsolved page, execute real unsolved material, score candidates, run search, or use CUDA.

## Next Stage

Stage 2I should prepare and review the first real bounded CPU exploratory approval packet without executing it unless explicit human approval is supplied later.

