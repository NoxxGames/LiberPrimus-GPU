# Stage 3G p56-local prime offset sweep

Stage 3G implements the bounded p56-local `prime_minus_one` offset sweep from the Stage 3E queue.

## Scope

- Queue item: `stage3e_prime_minus_one_offsets_v1`
- Input slice: `stage3a-page-candidate-018-reviewable-slice`
- Stream family: `prime_minus_one`
- Offsets: `0..63`
- Directions: `forward`, `reverse`
- Reset modes: `none`, `line`
- Candidate count: `64 * 2 * 2 = 256`
- Scoring: Stage 3C calibrated triage
- CUDA: disabled
- Solve claim: false

## Command

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run run-prime-offset-sweep `
  --policy experiments/policies/operator-policy-v0.yaml `
  --queue experiments/queues/stage3e-bounded-cpu-queue.yaml `
  --item-id stage3e_prime_minus_one_offsets_v1 `
  --out-dir experiments/results/bounded-auto-runs/stage3g `
  --top-k 25 `
  --allow-warnings
```

Summarize the generated local output:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run summary `
  --results-dir experiments/results/bounded-auto-runs/stage3g
```

## Output Policy

Generated records are local-only and ignored under `experiments/results/bounded-auto-runs/stage3g/`.

Committed research logs may summarize the run ID, candidate counts, top offset/direction/reset mode, score, calibrated label, and safety flags. They must not include full candidate dumps or claim a solve.

## Result

The Stage 3G local run executed `256 / 256` candidates with `0` deferred candidates. The top lead used offset `29`, direction `reverse`, reset mode `line`, score `1.36709`, and calibrated label `inconclusive`. The confidence distribution was mostly `garbage`, with a small `inconclusive` tail. This is not solve evidence.
