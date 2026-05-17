# Approval-Gated Execution Workflow

## Proposal

A Stage 2H proposal describes a control execution target while keeping `execution_enabled=false` in the proposal itself.

## Approval Record

The approval record supplies the explicit approval decision. Approved Stage 2H records are committed only for synthetic and solved-control proposals.

## Request

The request binds proposal, approval record, output directory, and requested execution scope.

## Plan

The plan records approval-gate status, blocking reasons, safety gates, execution manifest preview, and output paths.

## Run

Passing safe requests delegate to the Stage 2F execution harness. Blocked requests write blocked results and perform no execution.

## Result

Results record whether execution occurred, the safe scope, underlying control result ids, and false search/scoring/CUDA flags.

## Blocked Real Proposals

The no-op real proposal touches a future unsolved page candidate but has a pending approval and remains blocked.

## Generated-Output Policy

Generated Stage 2H plans and results are ignored under `experiments/results/approval-gated-execution/` and must not be committed.

