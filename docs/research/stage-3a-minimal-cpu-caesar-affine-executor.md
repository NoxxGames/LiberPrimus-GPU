# Stage 3A Minimal CPU Caesar Affine Executor

## Stage Goal

Stage 3A replaces the Stage 2J deferred result for the first 841-candidate queue item with a real bounded CPU execution path.

## Inputs

- `experiments/policies/operator-policy-v0.yaml`
- `experiments/queues/stage2j-bounded-cpu-queue.yaml`
- generated ignored corpus-candidate metadata for `rtkd-master-v0-candidate`

## Implementation

The new executor loads a reviewable index-29 slice, enumerates Caesar shift mod 29 and affine mod 29 candidates, applies minimal deterministic triage scoring, and writes ignored output records.

## Validation Result

The expected candidate count is `841`: Caesar `29` plus affine `812`. CUDA remains disabled, page boundaries remain reviewable, the canonical corpus remains inactive, and no solve claim is made.

## What This Proves

The workbench can now run a small real bounded CPU candidate enumeration under the standing operator policy and preserve generated outputs outside Git.

## What This Does Not Prove

It does not prove any candidate is correct. It does not start a broad search campaign, activate a canonical corpus, finalize page boundaries, implement CUDA, or publish a solution.

## Next Stage

Stage 3B should inspect Stage 3A top candidates as leads and either queue the next bounded method or improve scoring/null controls.
