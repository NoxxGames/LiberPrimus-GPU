# Stage 2G Experiment Proposal Approval Workflow

## Stage Goal

Prepare proposal, review, and explicit human-approval gates for future bounded CPU exploratory experiments.

## Inputs

Stage 2G builds on Stage 2E dry-run planning, Stage 2F safe execution controls, the transform registry, result-store policy, and CI consistency checks.

## Schemas

The stage adds `experiment-proposal-v0`, `experiment-review-packet-v0`, `experiment-approval-record-v0`, and `experiment-review-checklist-v0`.

## Proposals

Committed examples cover Caesar, affine, explicit-key Vigenere, prime-stream parameters, and a solved-fixture control. Every example is blocked pending human approval.

## Review Packets

Generated review packets summarize proposal bounds, safety gates, approval status, and risks. They are ignored outputs.

## Approval Gates

The approval gate blocks missing, pending, denied, invalid, expired, or mismatched approval records.

## Validation Result

Local and CI validation are recorded in the developer log and final task report.

## What This Stage Proves

The repository can represent and review future bounded exploratory experiments without executing them.

## What This Stage Does Not Prove

It does not solve any page, execute unsolved proposals, generate candidate plaintexts, score outputs, use CUDA, activate canonical corpus, or finalize page boundaries.

## Next Stage

Stage 2H should implement an approval-gated execution path for approved proposals, initially limited to synthetic/solved controls or a no-op real proposal.
