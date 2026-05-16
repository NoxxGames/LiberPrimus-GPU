# Exploratory Experiment Manifests

## Purpose

Exploratory manifests are human-readable YAML plans for future bounded CPU experiments. In Stage 2E they are dry-run only and are never execution manifests.

## Manifest Fields

Each manifest records `record_type`, `manifest_id`, `manifest_version`, stage, disabled execution flags, corpus slice, transform plan, parameter space, safety gates, expected candidate-count upper bound, result-store policy, output policy, provenance, and notes.

## Corpus Slice Model

Corpus slices may reference solved fixture groups, synthetic inputs, future review-required page candidates, or future selector ranges. Future unsolved page candidates must set `review_required=true`.

## Transform-Space Model

Transform spaces describe a transform family, optional registered transform ID, dry-run support, parameter bounds, a candidate-count formula, and an upper bound. Stage 2E supports count previews for direct, reverse, rotated reverse, Caesar, affine mod-29, Vigenere key-list, and prime-stream parameter spaces.

## Safety Gates

Safety gates require dry-run-only mode and block search execution, candidate generation, scoring, CUDA, canonical corpus activation, page-boundary finalization, and canonical trust.

## Candidate-Count Bounds

Every manifest includes `expected_candidate_count_upper_bound`. The dry-run planner fails if the estimated count exceeds that bound.

## Example Manifests

Examples live under `experiments/manifests/exploratory/` and cover direct known-fixture replay, Caesar preview, affine preview, Vigenere key-list preview, and prime-stream parameter preview.

## What Is Not Executed

The manifests do not decrypt unsolved pages, enumerate plaintexts, score candidates, or use CUDA.
