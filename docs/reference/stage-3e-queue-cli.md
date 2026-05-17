# Stage 3E Queue CLI

## Validate Queue

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-experiment validate-queue `
  --queue experiments/queues/stage3e-bounded-cpu-queue.yaml
```

## Check Policy

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-experiment check-queue `
  --policy experiments/policies/operator-policy-v0.yaml `
  --queue experiments/queues/stage3e-bounded-cpu-queue.yaml
```

## Dry Run Queue

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-experiment dry-run-queue `
  --policy experiments/policies/operator-policy-v0.yaml `
  --queue experiments/queues/stage3e-bounded-cpu-queue.yaml `
  --out-dir experiments/results/bounded-auto-runs/stage3e `
  --allow-warnings
```

The dry run validates deterministic candidate counts, operator-policy status, and executor support. It writes `stage3e_queue_dry_run_summary.json` under an ignored generated output path.

## Expected Stage 3E Summary

- `item_count=6`
- `total_candidate_estimate=780`
- `runnable_now_count=1` after Stage 3F implements the LP evidence-key Vigenere executor
- `needs_executor_count=3` after Stage 3F
- `dry_run_only_count=2`
- `blocked_count=0`

## Troubleshooting

If a count changes, inspect the corresponding queue item's exact parameters and update tests only when the manifest change is intentional. If an item needs an executor, leave it deferred until the executor is implemented and tested. Do not mark missing executors as runnable.
