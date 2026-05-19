# Stage 4B Visual Observation Intake

Stage 4B records visual and numeric leads as review-only observations. The purpose is to preserve exact claims, ambiguity, and stop conditions before any future annotation or experiment stage.

## Records

The committed record set is `data/observations/visual/stage4b-visual-observation-records.yaml`.

Current Stage 4B observations include:

- Cuneiform/base-60 candidate tuple `[17, 13, 55, 1]`, with derived values `1033`, `3301`, and `3722101`.
- Mirrored three-dot delimiter observations for page 5 and page 56.
- Ambiguous five-dot / three-dot binary readings, including forced 13/31 risk.
- Raw Interconnectedness / number-square source-lock target observations.
- Exact cookie artefact context for `167` and `761`.

## Guardrails

Every Stage 4B visual observation remains:

- `trusted_as_canonical=false`
- `usable_as_experiment_seed=false`
- `solve_claim=false`
- `review_status=human_review_required`

The cuneiform arithmetic may be internally consistent, but the visual segmentation is not verified. Dot, braille, constellation, and star interpretations require exact coordinates and ambiguity tables before they can become bounded experiment inputs.

## Next Step

Stage 4C should create a cuneiform and dot annotation pack with coordinates, alternate readings, review status, and negative controls.
