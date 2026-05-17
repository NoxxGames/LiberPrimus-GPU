# Stage 3J Mersenne / Perfect-Number Probe

Stage 3J executes the queued bounded Mersenne/perfect-number stream probe.

## Parameters

- Queue item: `stage3j_mersenne_prime_stream_tiny_v1`
- Candidate count: `192`
- Exponent sequence: `2`, `3`, `5`, `7`, `13`, `17`, `19`, `31`
- Stream variants: `mersenne_mod29`, `mersenne_minus_one_mod29`, `perfect_number_mod29`
- Offsets: `0..15`
- Directions: `forward`, `reverse`
- Reset modes: `none`, `line`
- Scoring: Stage 3C calibrated minimal triage

The exponent sequence is finite and cyclic. Duplicate stream signatures are expected and must be reported.

## Command

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-run run-mersenne-stream-probe `
  --policy experiments/policies/operator-policy-v0.yaml `
  --queue experiments/queues/stage3j-bounded-cpu-queue.yaml `
  --item-id stage3j_mersenne_prime_stream_tiny_v1 `
  --out-dir experiments/results/bounded-auto-runs/stage3j `
  --top-k 25 `
  --allow-warnings
```

Generated outputs are ignored under `experiments/results/bounded-auto-runs/stage3j/`.

## Result

The local run executed all `192` candidates with `0` deferred. It produced `96` unique stream signatures and `96` duplicate signatures.

Top lead: `perfect_number_mod29`, offset `3`, direction `forward`, reset `none`, score `1.515716`, calibrated label `inconclusive`.

This is not solve evidence.
