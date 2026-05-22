# Stage 5AB Source Of Truth Summary

Stage 5AB adds two project-state records that future operational checks can cite:

- `data/project-state/stage5ab-doc-staleness-source-of-truth.yaml`
- `data/project-state/operational-file-map.yaml`

The source-of-truth record states:

- Latest completed stage after repair: Stage 5AB - markdown staleness detection hardening and stale-doc repair.
- Expected next stage: Stage 5AC - selected from Stage 5AA outcome after stale-doc repair.
- Website expansion: deferred future unnumbered project.
- Unsolved-page CUDA: blocked.
- Canonical corpus: inactive.
- Page boundaries: reviewable.

The operational file map separates mutable current-state docs from historical logs and wiki mirrors. This lets the scanner be strict on active docs while preserving old stage history in development logs and research logs.
