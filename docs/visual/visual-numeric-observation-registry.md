# Visual Numeric Observation Registry

Stage 3K records visual numeric observations in `data/observations/visual/visual-numeric-observations-v0.yaml`.

The registry preserves ambiguity. Cuneiform/base-60 readings, binary-dot readings, prime-dimension examples, and numeric table placeholders are reviewable hypotheses. They are not experiment seeds by default.

All visual observation records must keep:

- `trusted_as_canonical=false`
- `usable_as_experiment_seed=false`
- an explicit confidence label
- ambiguity notes

Future stages may promote a reviewed observation into a bounded experiment seed only through a manifest and policy check.
