# Stage 3B Lead Inspection And Scoring Refinement

## Goal

Inspect Stage 3A Caesar plus affine leads, reduce obvious scoring false positives, and queue the next bounded CPU method.

## Inputs

- Stage 3A ignored candidate outputs under `experiments/results/bounded-auto-runs/stage3a/`
- Stage 3A committed summary log
- Standing operator policy

## Findings

The Stage 3A original top lead is weak/noisy. It has no separator or space context and appears to be rewarded by accidental short embedded common-word fragments.

Refined scoring changes the top lead and lowers the confidence label to `noisy`.

## Next Method

Stage 3B adds `experiments/queues/stage3b-bounded-cpu-queue.yaml` with a reverse-direction Caesar plus affine item, a rerank control, and an over-budget blocked control.

The reverse-direction run executed within policy and also produced a `noisy` top label.

## Non-Claims

No solve claim is made. Full candidate dumps remain ignored. CUDA is not used. The canonical corpus remains inactive and page boundaries remain reviewable.
