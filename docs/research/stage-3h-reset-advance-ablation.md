# Stage 3H Reset/Advance Ablation Research Note

Stage 3H tested whether reset and token-advance semantics are worth prioritizing before widening transform families.

The bounded run executed `64` of `64` planned reset/advance candidates on the existing reviewable slice. The top candidate used `prime_minus_one:offset=1`, reset `line`, and advance `runes_only`, with calibrated confidence `noisy`. The run generated `100` ignored family-specific negative controls.

This is not solve evidence. The useful outcome is that the shared reset/advance state machine now records metadata support explicitly and can defer missing word, clause, or line modes instead of inventing boundaries.
