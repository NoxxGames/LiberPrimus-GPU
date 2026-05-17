# Stage 2J Bounded Auto-Run Policy

## Stage Goal

Stage 2J simplifies experiment workflow by replacing per-experiment approval as the default path with a standing bounded local CPU policy.

## Inputs

- Stage 2I first bounded Caesar plus affine proposal.
- Stage 2F solved-baseline control infrastructure.
- Existing ignored generated result directories.

## Schemas

Stage 2J adds schemas for operator policies, bounded experiment queues, bounded experiment items, policy-check results, and bounded auto-run results.

## Queue

The first queue contains a policy-eligible `841` candidate Caesar plus affine reviewable-slice item, a solved-baseline regression control, and an intentionally blocked over-budget item.

## Validation Result

Policy checks distinguish allowed bounded local CPU work from over-budget or high-risk work. CUDA, cloud, generated-output commits, canonical corpus activation, page-boundary finalization, and solve claims remain blocked.

## What This Stage Proves

The workbench can now evaluate and queue bounded CPU experiments under a standing policy without a per-experiment approval ritual.

## What This Stage Does Not Prove

Stage 2J does not execute real unsolved candidate transforms, score candidates, use CUDA, activate canonical corpus, finalize page boundaries, or claim solves.

## Next Stage

If the first real item remains deferred, Stage 3A should implement the minimal real transform execution/scoring scaffold needed for the `841` candidate Caesar plus affine queue item.
