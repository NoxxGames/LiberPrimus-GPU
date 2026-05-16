# Experiment Approval Workflow

## Purpose

Stage 2G adds the approval paperwork for future bounded CPU exploratory experiments. It defines proposal records, review checklists, approval records, review packets, and a hard approval gate.

## Why Approval Gates Exist

Real unsolved-page execution is higher risk than synthetic or solved-fixture replay. It needs explicit human review of the corpus slice, transform family, candidate-count bounds, result-store policy, rollback plan, and stop conditions before any run.

## Proposal Lifecycle

Proposals start as `draft` or `ready_for_review`. Stage 2G examples remain blocked with `approved_for_execution=false` and `execution_enabled=false`.

## Approval Records

Approval records model `pending`, `approved`, `denied`, `expired`, and `superseded` decisions. Future approved records must include proposal SHA-256, approver, timestamp, scope, constraints, and expiry.

## Review Packets

Review packets are generated summaries for human review. They include proposal bounds, safety gates, dry-run context when available, risk notes, and the exact approval status.

## Execution Block Policy

No proposal can execute without a valid approved approval record. Pending, denied, missing, expired, mismatched, or incomplete records block execution.

## Future Transition To Approved Execution

Stage 2H may add an approval-gated execution path, initially for synthetic/solved controls or a no-op real proposal.

## Non-Goals

Stage 2G does not execute proposals, generate candidates, score outputs, use CUDA, activate canonical corpus, or finalize page boundaries.
