# Prime Offset Sweep CLI

Stage 3G adds:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run run-prime-offset-sweep `
  --policy experiments/policies/operator-policy-v0.yaml `
  --queue experiments/queues/stage3e-bounded-cpu-queue.yaml `
  --item-id stage3e_prime_minus_one_offsets_v1 `
  --out-dir experiments/results/bounded-auto-runs/stage3g `
  --top-k 25 `
  --allow-warnings
```

The command validates the standing operator policy, loads the queue item, enumerates the declared p56-local offsets, directions, and reset modes, scores candidates with calibrated triage, and writes ignored generated outputs.

Summary command:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run summary `
  --results-dir experiments/results/bounded-auto-runs/stage3g
```

Expected Stage 3G fields include:

- `expected_candidate_count=256`
- `executed_candidate_count`
- `deferred_candidate_count`
- `prime_candidate_count`
- `top_candidate_offset`
- `top_candidate_direction`
- `top_candidate_reset_mode`
- `solve_claim=false`

Line reset candidates are deferred only if line metadata is missing. The Stage 3G run used available token metadata and executed all `256` candidates.
