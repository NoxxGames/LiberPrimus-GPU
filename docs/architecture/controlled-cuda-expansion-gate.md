# Controlled CUDA Expansion Gate

Stage 5N records explicit gates between the Stage 5M exact solved-fixture parity pass and any later CUDA work.

Gate outcomes:

- `exact_repeat_verification_gate`: approved only for a future exact repeat of the same five Stage 5L buffers.
- `additional_solved_fixture_shift_score_gate`: needs candidate selection, source-backed token mappings, native hashes, and explicit future-stage approval.
- `result_store_score_summary_gate`: needs Stage 5O result-store and score-summary preflight.
- `broad_solved_fixture_cuda_gate`: blocked as too broad.
- `unsolved_page_cuda_gate`: blocked because the canonical corpus is inactive, page boundaries are reviewable, and no broad CUDA campaign is approved.

The gate is not execution permission except where a later stage explicitly scopes that execution.
