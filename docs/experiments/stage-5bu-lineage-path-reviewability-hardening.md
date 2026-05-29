# Stage 5BU Lineage-Path Reviewability Hardening

Stage 5BU is not an experiment. It is a metadata repair and reviewability hardening
stage for the Stage 5BS planning-ingestion gate.

The concrete repair is the Stage 5BS preserved active-lineage path for the Stage 5AW
repaired branch manifest:

- Deprecated path: `data/token-block/stage5aw-repaired-branch-manifest.yaml`
- Correct path: `data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml`

Stage 5BU records the repair with an erratum, preserved active-lineage digest index,
path-resolution validation, and Stage 5BS validator hardening. The String 4 planning
ingestion gate remains closed and future token-block execution remains blocked.

Generated diagnostics under `experiments/results/token-block/stage5bu/` are ignored and
must not be committed.
