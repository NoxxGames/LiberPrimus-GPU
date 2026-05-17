# Stage 3E Method Backlog

## Purpose

Stage 3E ingests the Deep Research method backlog as planning metadata for bounded CPU experiments. It turns evidence-ranked ideas into committed queue records with exact parameters, deterministic candidate counts, output policy, and executor-support status.

This is not a solve claim, broad search campaign, CUDA task, canonical corpus activation, or page-boundary finalization.

## Backlog Source

The integrated research input is stored at `docs/research/LiberPrimus-CPU-Research-Backlog-For-LiberPrimus-GPU.md`.

The machine-readable backlog is `experiments/queues/stage3e-method-backlog.yaml`.

## Backlog Items

The Stage 3E backlog started with six candidate method families. Stage 3G adds one future low-cost probe:

- `stage3e_vig_lp_evidence_pack_v1`: LP evidence Vigenere key pack, `48` candidates.
- `stage3e_prime_minus_one_offsets_v1`: p56-local prime-minus-one offset sweep, `256` candidates.
- `stage3e_vig_history_key_pack_v1`: historical motif Vigenere key pack, `56` candidates.
- `stage3e_negative_control_extension_v1`: family-specific negative controls, `100` candidates.
- `stage3e_reset_advance_ablation_v1`: reset/advance ablation dry-run, `64` candidates.
- `stage3e_prime_mod_gap_pack_v1`: prime neighbour stream dry-run, `256` candidates.
- `stage3i_mersenne_prime_stream_tiny_v1`: future Mersenne/perfect-number stream probe, `192` candidates, `needs_executor`.

Total deterministic candidate estimate after Stage 3G: `972`.

## Scope Controls

Each item declares:

- exact transform parameters;
- evidence basis;
- candidate-count estimate;
- implementation status;
- required controls;
- generated-output policy;
- `cuda_enabled=false`;
- `no_solve_claim=true`;
- `canonical_corpus_active=false`;
- `page_boundaries_final=false`.

Items that need missing executors stay deferred. Stage 3E does not fake candidate output.
