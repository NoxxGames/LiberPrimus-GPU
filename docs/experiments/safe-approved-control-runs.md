# Safe Approved Control Runs

## Synthetic Approved Controls

The synthetic direct control proves that an approved request can cross the approval gate and execute a safe Stage 2F synthetic manifest.

## Solved-Fixture Replay Controls

The solved replay control proves that already known solved-fixture regression can be approval-gated without treating it as a new solve.

## Why No Unsolved Approval Records Are Committed

Stage 2H tests approval machinery only. Approved records for real unsolved-page execution are out of scope and would require a future explicit instruction.

## How To Review Outputs

Run `libreprimus approval-execution summary --results-dir experiments/results/approval-gated-execution/stage2h` after local smoke checks. Generated outputs are ignored and may be deleted safely.

