# Stage 3E Method Backlog Ingestion

## Stage Goal

Stage 3E ingests the method-prioritization backlog, converts the top recommendations into bounded queue records, validates counts, and classifies executor readiness.

## Inputs

- Stage 3A/3B Caesar and affine leads: noisy.
- Stage 3C scoring calibration: Stage 3A/3B leads remain noisy.
- Stage 3D four-key Vigenere preview: top key `LIBER`, confidence `noisy`.
- Deep Research backlog input: `docs/research/LiberPrimus-CPU-Research-Backlog-For-LiberPrimus-GPU.md`.

## Outputs

- `experiments/queues/stage3e-method-backlog.yaml`
- `experiments/queues/stage3e-bounded-cpu-queue.yaml`
- `schemas/experiments/method-backlog-v0.schema.json`
- `schemas/experiments/method-backlog-item-v0.schema.json`
- `schemas/experiments/stage3e-queue-item-v0.schema.json`

## Validation Result

The Stage 3E queue contains six items with total deterministic candidate estimate `780`. All items fit the standing operator policy. No item executed because required executors are missing or dry-run-only.

## What This Proves

The workbench can convert research recommendations into bounded, count-checked, policy-checked experiment queues without silently broadening scope.

## What This Does Not Prove

It does not test the queued transforms, generate candidates, score outputs, use CUDA, activate canonical corpus, finalize page boundaries, or solve a page.

## Next Stage

Stage 3F should implement the reset/advance-aware evidence-key Vigenere pack executor and run the LP evidence pack if it remains within policy.
