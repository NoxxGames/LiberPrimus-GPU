# Stage 4C Cuneiform And Dot Annotation Pack

Stage 4C turns Stage 4B visual observations into reviewable annotation tasks. It does not decide what the visual motifs mean.

Committed records live under `data/observations/visual/`:

- `stage4c-visual-annotation-tasks.yaml`
- `stage4c-cuneiform-reading-candidates.yaml`
- `stage4c-dot-pattern-annotation-tasks.yaml`
- `stage4c-delimiter-annotation-tasks.yaml`
- `stage4c-visual-negative-control-annotation-tasks.yaml`
- `stage4c-annotation-pack-summary.yaml`

Generated local review output lives under `experiments/results/visual-annotation/stage4c/` and remains ignored. The generated site contains page/task views, grid overlays, and blank coordinate templates for human review.

## Boundary

A coordinate annotation can show that a region exists on an image. It does not prove a cuneiform reading, binary reading, delimiter meaning, reset boundary, or cipher seed.

All Stage 4C records keep:

- `trusted_as_canonical=false`
- `usable_as_experiment_seed=false`
- `solve_claim=false`

The cuneiform tuple `[17, 13, 55, 1]` remains a candidate only. Dot readings such as `13` and `31` remain ambiguous and unforced. Braille, constellation, forced dot-value, and visual-overfit classes remain negative controls unless a later review stage supplies exact coordinates, alternatives, and null controls.
