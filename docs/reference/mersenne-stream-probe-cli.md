# Mersenne Stream Probe CLI

Run the Stage 3J bounded Mersenne/perfect-number probe:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run run-mersenne-stream-probe `
  --policy experiments/policies/operator-policy-v0.yaml `
  --queue experiments/queues/stage3j-bounded-cpu-queue.yaml `
  --item-id stage3j_mersenne_prime_stream_tiny_v1 `
  --out-dir experiments/results/bounded-auto-runs/stage3j `
  --top-k 25 `
  --allow-warnings
```

Print the generated summary:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run summary `
  --results-dir experiments/results/bounded-auto-runs/stage3j
```

The command writes generated JSON/JSONL records only under ignored output paths. Terminal output and top-ranked candidates are leads only, not solve evidence.
