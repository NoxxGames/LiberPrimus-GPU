# Stage 2E CPU Exploratory Dry-Run Planner

## Stage Goal

Stage 2E creates schema, manifest, CLI, and safety-gate infrastructure for future bounded CPU exploratory experiments without executing those experiments.

## Inputs

Inputs are committed schemas, transform registry metadata, solved fixture references, and dry-run-only exploratory manifests.

## Schemas Created

Stage 2E adds schemas for exploratory manifests, corpus slices, transform spaces, safety gates, and dry-run plans.

## Manifests Created

Committed manifests cover direct known-fixture replay, Caesar preview, affine preview, Vigenere key-list preview, prime-stream parameter preview, and an index of the Stage 2E preview manifests.

## Candidate Estimators

The estimator counts bounded parameter spaces: direct `1`, Caesar `29`, affine mod-29 `812`, explicit Vigenere key list length, and explicit prime-stream parameter products.

## Safety Gates

Safety gates require dry-run-only mode and reject enabled execution, search, candidate generation, scoring, CUDA, canonical corpus activation, page-boundary finalization, canonical trust, missing bounds, over-bound estimates, and unsafe output paths.

## Validation Result

Validation is recorded in the Stage 2E developer log and final task report.

## What This Stage Proves

Stage 2E proves that future exploratory CPU experiment paperwork can be validated, bounded, and planned in CI without raw data and without execution.

## What This Stage Does Not Prove

It does not solve an unsolved page, run search, generate candidates, score results, implement CUDA, activate the canonical corpus, or finalize page boundaries.

## Next Stage

Stage 2F should design a bounded CPU experiment execution harness for synthetic and solved-fixture-only runs while still prohibiting unsolved-page campaigns.
