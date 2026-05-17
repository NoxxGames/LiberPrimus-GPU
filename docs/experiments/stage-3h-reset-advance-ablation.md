# Stage 3H Reset/Advance Ablation

Stage 3H runs `stage3h_reset_advance_ablation_v1` from `experiments/queues/stage3h-bounded-cpu-queue.yaml`.

The ablation tests eight base transforms across four reset modes and two advance modes for `64` candidates:

- Vigenere keys: `DIVINITY`, `FIRFUMFERENFE`, `PATIENCEISAVIRTUE`, `THEINSTAREMERGENCE`.
- Prime streams: `prime_minus_one` offsets `0` and `1`, `prime_mod29` offset `0`, and `prime_gap` offset `0`.
- Reset modes: `none`, `word`, `clause`, `line`.
- Advance modes: `runes_only`, `token_break_preserving`.

The Stage 3A reviewable slice metadata supported word, clause, line, and token-break handling, so the local run executed all `64` candidates and deferred `0`. It also wrote `100` family-specific negative controls. Full generated outputs are ignored under `experiments/results/bounded-auto-runs/stage3h/`.

Top candidates remain triage leads only. Stage 3H makes no solve claim.
