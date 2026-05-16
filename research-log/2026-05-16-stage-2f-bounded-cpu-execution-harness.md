# Stage 2F Bounded CPU Execution Harness

## Status

Complete pending remote CI verification.

## Goal

Add a CPU-only execution harness that is restricted to synthetic and solved-fixture-only manifests.

## Result

Stage 2F adds execution schemas, safe manifests, a blocked unsolved negative manifest, safety gates, CLI commands, generated output support, and CI-covered validation for bounded CPU execution.

Local validation passed with `383` Python tests, `109` consistency checks, public documentation checks, lock-hash checks, workflow-static checks, and the Stage 2F execution smoke. The smoke produced `6` safe pass results and rejected `1` blocked unsolved manifest.

## What This Does Not Do

It does not run unsolved-page experiments, generate unsolved-page candidate plaintexts, score candidates, use CUDA, activate a canonical corpus, or finalize page boundaries.

## Next Stage

Stage 2G should prepare the first bounded CPU exploratory experiment proposal and approval workflow with explicit human approval before any real unsolved-page execution.
