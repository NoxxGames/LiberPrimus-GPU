# Reset/Advance Ablation CLI

Run the Stage 3H ablation:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run run-reset-advance-ablation `
  --policy experiments/policies/operator-policy-v0.yaml `
  --queue experiments/queues/stage3h-bounded-cpu-queue.yaml `
  --item-id stage3h_reset_advance_ablation_v1 `
  --out-dir experiments/results/bounded-auto-runs/stage3h `
  --top-k 25 `
  --allow-warnings
```

Summarize generated local results:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run summary `
  --results-dir experiments/results/bounded-auto-runs/stage3h
```

The command writes ignored generated files: `candidate_records.jsonl`, `top_candidates.jsonl`, `negative_control_records.jsonl`, `summary.json`, `warnings.jsonl` when needed, and score details. Do not commit these files.
