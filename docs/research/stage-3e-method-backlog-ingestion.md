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

The Stage 3E queue initially contained six items with total deterministic candidate estimate `780`. Stage 3G added the future Mersenne/perfect-number probe, bringing the current queue to seven items with total deterministic candidate estimate `972`. Stage 3J promotes that probe to runnable through a bounded executor. All items fit the standing operator policy. Items without executors remain deferred or dry-run-only instead of being faked as runnable.

## What This Proves

The workbench can convert research recommendations into bounded, count-checked, policy-checked experiment queues without silently broadening scope.

## What This Does Not Prove

It does not test the queued transforms, generate candidates, score outputs, use CUDA, activate canonical corpus, finalize page boundaries, or solve a page.

## Next Stage

Stage 3F implemented the reset/advance-aware evidence-key Vigenere pack executor. Stage 3G implemented the p56-local prime offset executor. The next bounded stage should focus on reset/advance ablation, family-specific negative controls, or careful inspection of Stage 3G leads.
