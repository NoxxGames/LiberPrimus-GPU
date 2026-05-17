# Stage 3E Method Backlog Ingestion

## Summary

Stage 3E ingested the Deep Research method backlog into committed machine-readable records. The backlog is a research input and queue plan, not a solve claim.

## Backlog Path

- Research input: `docs/research/LiberPrimus-CPU-Research-Backlog-For-LiberPrimus-GPU.md`
- Machine backlog: `experiments/queues/stage3e-method-backlog.yaml`
- Bounded queue: `experiments/queues/stage3e-bounded-cpu-queue.yaml`

## Items

- `stage3e_vig_lp_evidence_pack_v1`: `48` candidates, needs reset/advance key-pack executor.
- `stage3e_prime_minus_one_offsets_v1`: `256` candidates, needs prime offset sweep executor.
- `stage3e_vig_history_key_pack_v1`: `56` candidates, needs reset/advance key-pack executor.
- `stage3e_negative_control_extension_v1`: `100` candidates, needs family-specific negative-control executor.
- `stage3e_reset_advance_ablation_v1`: `64` candidates, dry-run-only.
- `stage3e_prime_mod_gap_pack_v1`: `256` candidates, dry-run-only.

Total deterministic candidate estimate: `780`.

## Safety

All items keep `cuda_enabled=false`, `no_solve_claim=true`, `canonical_corpus_active=false`, and `page_boundaries_final=false`. Generated outputs remain ignored. No item executed in this ingestion stage.

## Next Stage

Stage 3F should implement the reset/advance-aware evidence-key Vigenere pack executor and run only the LP evidence pack if it remains policy-compliant.
