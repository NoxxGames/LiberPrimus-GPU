# Dry-Run Planner

## Purpose

The Stage 2E dry-run planner validates exploratory manifests and writes generated plan records that describe what a future bounded experiment would do.

## CLI Commands

- `libreprimus experiment validate-exploratory`
- `libreprimus experiment dry-run`
- `libreprimus experiment stage2e-dry-run-all`
- `libreprimus experiment dry-run-summary`

## Dry-Run Outputs

Generated outputs are written under `experiments/results/exploratory-dry-runs/stage2e/` by default. The planner writes one plan JSON file, one safety-gates JSONL file per manifest, and a summary JSON for multi-manifest runs.

## Safety Failure Behaviour

Any failed safety gate returns a non-zero exit. Warnings can be allowed explicitly, but execution/search/scoring/CUDA gates are hard failures.

## Generated-Output Policy

Generated dry-run outputs are ignored by Git and must not be staged or committed.

## CI Usage

CI validates committed exploratory manifests through the consistency suite and performs a raw-data-free Caesar dry-run into a temporary runner directory.
