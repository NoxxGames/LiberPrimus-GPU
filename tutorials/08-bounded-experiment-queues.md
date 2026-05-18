# Bounded Experiment Queues

## Purpose

Run policy-approved local CPU experiments without broadening into campaigns.

## Commands

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-experiment validate-policy `
  --policy experiments/policies/operator-policy-v0.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-experiment dry-run-stage3e `
  --policy experiments/policies/operator-policy-v0.yaml `
  --queue experiments/queues/stage3e-bounded-cpu-queue.yaml `
  --out experiments/results/bounded-auto-runs/stage3e/stage3e_queue_dry_run_summary.json `
  --allow-warnings
```

## Expected Outputs

Policy checks should pass for bounded CPU-only items and fail for over-budget examples.

## What Not To Commit

Do not commit generated candidate dumps, top-candidate JSONL, SQLite files, or broad-search outputs.

## Troubleshooting

If a queue item lacks an executor, record it as deferred instead of faking output.
