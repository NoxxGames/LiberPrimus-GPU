# Synthetic And Solved-Only Execution

## Synthetic Execution

Synthetic examples exercise registered CPU reference transforms on tiny token records that do not contain unsolved Liber Primus text.

## Solved-Fixture Replay

Solved-fixture replay validates the known solved-baseline path. It is regression evidence only and does not make new solve claims.

## Why Unsolved Execution Is Blocked

The canonical corpus is inactive and page boundaries remain reviewable. Any future real exploratory run must go through a separate proposal and approval stage.

## Inspecting Outputs

Run `libreprimus execution summary --results-dir experiments/results/cpu-execution/stage2f` after local execution smoke commands to inspect generated summary counts.

## Generated-Output Policy

Generated Stage 2F outputs are ignored by Git. Do not stage JSON, JSONL, SQLite, or database sidecar files from execution runs.
