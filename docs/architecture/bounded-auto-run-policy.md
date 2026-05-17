# Bounded Auto-Run Policy

## Purpose

Stage 2J replaces per-experiment approval as the normal path for small local CPU work. The operator policy grants standing permission for bounded experiments that fit hard limits and safety constraints.

## Policy Shape

The committed policy is `experiments/policies/operator-policy-v0.yaml`. It permits local CPU-only automation when candidate count, runtime, and generated-output budget remain within limits.

Current limits:

- Candidate upper bound: `100000`
- Runtime estimate: `600` seconds
- Generated output budget: `250` MB
- CUDA, cloud execution, and paid services: disabled

## Hard Blocks

The policy blocks or requires explicit user instruction for over-budget work, CUDA or GPU campaigns, cloud or paid services, committing generated outputs, canonical corpus activation, page-boundary finalization, and solve claims.

## Queue Runner

The bounded runner loads an operator policy and a queue, evaluates each enabled item, and runs only items that pass policy. Generated records are written to ignored result directories.

Stage 2J does not invent missing executors. The first real Caesar plus affine queue item is policy-eligible but deferred until a safe real transform execution scaffold exists.

## Result Records

Generated `bounded_auto_run_result` records report whether execution happened, candidate count, policy status, and blocked or deferred reasons. They are generated outputs and must not be committed.

## Non-Goals

Stage 2J does not add CUDA, scoring, broad brute force, cloud work, canonical corpus activation, page-boundary finalization, or solve claims.
