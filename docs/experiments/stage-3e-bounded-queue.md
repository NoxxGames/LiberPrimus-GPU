# Stage 3E Bounded Queue

## Queue File

The bounded queue is `experiments/queues/stage3e-bounded-cpu-queue.yaml`.

It targets the same reviewable Stage 3A slice metadata unless a later manifest changes that explicitly. The queue stores metadata and dry-run policy only; it does not include raw unsolved text.

## Dry Run

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-experiment dry-run-queue `
  --policy experiments/policies/operator-policy-v0.yaml `
  --queue experiments/queues/stage3e-bounded-cpu-queue.yaml `
  --out-dir experiments/results/bounded-auto-runs/stage3e `
  --allow-warnings
```

Generated dry-run summaries are ignored under `experiments/results/bounded-auto-runs/stage3e/`.

## Stage 3E Status

Dry-run result:

- queue items: `6`;
- total candidate estimate: `780`;
- policy-blocked items: `0`;
- runnable-now items after Stage 3F: `1`;
- needs-executor items after Stage 3F: `3`;
- dry-run-only items: `2`;
- executed items: `0`.

Stage 3E itself executed no items. Stage 3F later implemented the LP evidence-key Vigenere executor and marked `stage3e_vig_lp_evidence_pack_v1` runnable.

## Executor Status

- `stage3e_vig_lp_evidence_pack_v1`: needs `reset_advance_key_pack_executor`.
- `stage3e_prime_minus_one_offsets_v1`: needs `prime_offset_sweep_executor`.
- `stage3e_vig_history_key_pack_v1`: needs `reset_advance_key_pack_executor`.
- `stage3e_negative_control_extension_v1`: needs `family_specific_negative_control_executor`.
- `stage3e_reset_advance_ablation_v1`: dry-run-only until a reset/advance state machine exists.
- `stage3e_prime_mod_gap_pack_v1`: dry-run-only until prime-neighbour stream executors exist.

## Next Step

Stage 3F should implement the reset/advance-aware evidence-key Vigenere pack executor and run only `stage3e_vig_lp_evidence_pack_v1` if it still passes operator-policy checks.
