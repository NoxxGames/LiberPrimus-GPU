# Reset/Advance State Machine

Stage 3H adds a shared CPU-only state machine for bounded reset and advance experiments.

The state machine accepts token records with transformable rune/index tokens plus optional separator metadata. Reset modes are `none`, `word`, `clause`, and `line`. Advance modes are `runes_only` and `token_break_preserving`.

Missing metadata is not invented. If a reset mode needs absent word, clause, or line boundaries, the candidate is deferred with a specific reason such as `line_reset_metadata_missing`. If token-break metadata is absent but a flat sequence can still run, the candidate records `token_break_metadata_missing_flat_mode_used`.

Stage 3H uses the state machine for Vigenere, prime-minus-one, prime modulo-29, and prime-gap adapters. It remains a bounded local CPU experiment only: no CUDA, no broad search, no canonical corpus activation, no page-boundary finalization, and no solve claim.
