# Family-Specific Negative Controls

Stage 3H adds family-specific negative controls for reset/advance experiments. Controls are generated locally and deterministically from representative bounded candidate outputs.

The current controls are:

- `rune_shuffle_same_length`
- `rune_freq_preserving_shuffle`
- `separator_randomised_variant`
- `wrong_mapping_variant`

The Stage 3H run generated `100` controls, with `25` representatives for each control kind. These controls are scored with the same calibrated triage path used for candidates, but they are not evidence of plaintext and are not committed as generated JSONL output.

The purpose is false-positive pressure. If controls can receive high labels, the scorer must be treated as noisy until follow-up calibration improves it.
