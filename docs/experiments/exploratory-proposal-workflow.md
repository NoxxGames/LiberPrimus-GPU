# Exploratory Proposal Workflow

## Proposal Fields

`experiment_proposal` records define a title, proposed stage, corpus slice, transform space, parameter bounds, candidate-count estimate, upper bound, result-store policy, rollback plan, review checklist, provenance, and notes.

## Review Checklist

Each proposal includes an `experiment_review_checklist` with pending blocking items until a human reviewer makes an explicit decision.

## Candidate-Count Bounds

Stage 2G proposals carry bounded estimates only. They do not enumerate candidate plaintexts or execute transforms.

## Safety Gates

`execution_enabled`, `search_execution_enabled`, `candidate_generation_enabled`, `scoring_enabled`, and `cuda_enabled` remain false.

## Approval Status

`approved_for_execution=false` is required for committed Stage 2G examples. Pending and denied approval records are examples only and block execution.

## Generated Review Packets

Review packets are ignored generated outputs under `experiments/results/proposal-reviews/stage2g/`.

## Difference From Execution Manifests

Proposal files request review. CPU execution manifests run only synthetic or solved-fixture controls. Stage 2G proposals do not execute.
