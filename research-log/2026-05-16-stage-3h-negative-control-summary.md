# Stage 3H Negative Control Summary

Stage 3H generated family-specific negative controls from representative reset/advance candidates.

- Control count: `100`
- Control kinds: `rune_shuffle_same_length`, `rune_freq_preserving_shuffle`, `separator_randomised_variant`, `wrong_mapping_variant`
- Count per control kind: `25`
- Calibrated labels: `garbage=32`, `inconclusive=3`, `noisy=46`, `positive_control_like=3`, `weak_lead=16`

The presence of high labels among negative controls means Stage 3H scoring remains noisy and should not be used as solve evidence. Generated control records remain ignored under `experiments/results/bounded-auto-runs/stage3h/`.

Recommended next stage: Stage 3I should either implement the tiny Mersenne/perfect-number stream probe or use the now-available reset/advance executor for the historical Vigenere pack, depending on which bounded path is selected for follow-up.
