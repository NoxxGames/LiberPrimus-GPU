# Stage 2F Bounded CPU Execution Harness

## Stage Goal

Add a CPU execution harness limited to synthetic inputs and solved-fixture replay.

## Inputs

Inputs are committed CPU execution manifests, synthetic token records, the Stage 2A transform registry, and the Stage 2A solved-baseline manifest.

## Schemas

Stage 2F adds CPU execution manifest, plan, result, synthetic corpus record, and safety gate schemas.

## Manifests

The stage adds five synthetic execution manifests, one solved-baseline replay manifest, and one blocked unsolved negative-control manifest.

## Execution Harness

Synthetic execution dispatches one registered CPU transform per manifest. Solved-fixture replay records expected solved-baseline counts without touching unsolved corpus data.

## Safety Gates

Safety gates block unsolved execution, search, candidate generation, scoring, CUDA, canonical corpus activation, page-boundary finalization, unsafe output paths, and unsafe transforms.

## Validation Result

Local validation must include Ruff, pytest, smoke, consistency checks, lock verification, workflow static validation, and Stage 2F execution smoke.

## What This Stage Proves

The project can run bounded synthetic and solved-fixture CPU execution through manifest and safety-gate machinery.

## What This Stage Does Not Prove

It does not prove any unsolved-page plaintext, scorer, search campaign, CUDA kernel, canonical corpus, or final page boundary.

## Next Stage

Stage 2G should prepare the first bounded CPU exploratory experiment proposal and approval workflow.
