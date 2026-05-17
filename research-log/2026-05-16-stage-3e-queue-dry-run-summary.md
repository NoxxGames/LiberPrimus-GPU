# Stage 3E Queue Dry-Run Summary

## Dry Run

Command:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-experiment dry-run-queue `
  --policy experiments/policies/operator-policy-v0.yaml `
  --queue experiments/queues/stage3e-bounded-cpu-queue.yaml `
  --out-dir experiments/results/bounded-auto-runs/stage3e `
  --allow-warnings
```

## Counts

- Queue items: `6`
- Total candidate estimate: `780`
- Runnable now: `0`
- Needs executor: `4`
- Dry-run only: `2`
- Policy blocked: `0`
- Executed: `0`

## Deferred Reasons

- LP evidence Vigenere and historical Vigenere need `reset_advance_key_pack_executor`.
- p56-local prime-minus-one offsets need `prime_offset_sweep_executor`.
- Family-specific negative controls need `family_specific_negative_control_executor`.
- Reset/advance ablation and prime mod/gap pack are dry-run-only until their state-machine or stream executors exist.

## Generated Outputs

Generated dry-run output is local and ignored under `experiments/results/bounded-auto-runs/stage3e/`.

## No Solve Claim

No candidates were generated, no scoring output was produced, no CUDA was used, and no solve claim is made.
