# Coordinate Annotation Guide

Use the generated Stage 4C site at:

`experiments/results/visual-annotation/stage4c/site/index.html`

The site is local generated output. It is not committed.

## Manual Coordinate Capture

For each task:

1. Open the task page.
2. Open the linked page image.
3. Use the grid-overlay page to estimate a bounding box.
4. Fill the generated blank template for that task.
5. Record `x_min`, `y_min`, `x_max`, and `y_max`.
6. Record whether the coordinate system is `pixel_absolute` or `normalized_0_1`.
7. Record accepted and rejected readings separately.

Do not change `trusted_as_canonical`, `usable_as_experiment_seed`, or `solve_claim` while filling coordinate templates. A later review/promotion stage must make any status change explicitly.
