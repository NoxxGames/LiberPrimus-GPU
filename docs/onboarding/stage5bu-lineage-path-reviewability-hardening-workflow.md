# Stage 5BU Lineage-Path Reviewability Hardening Workflow

Use this workflow when reviewing the Stage 5BS lineage-path repair.

1. Confirm `data/token-block/stage5bs-active-manifest-preservation.yaml` cites
   `data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml`.
2. Run `python -m libreprimus.cli token-block validate-stage5bu-lineage-paths`.
3. Run `python -m libreprimus.cli token-block validate-stage5bu`.
4. Run `python -m libreprimus.cli token-block validate-stage5bs` to confirm the
   hardened Stage 5BS validator still passes after the repair.
5. Treat `codex-output/stage5bu-codex-completion.md` and
   `experiments/results/token-block/stage5bu/` as ignored local evidence only.

This stage does not authorize active String 4 ingestion, byte-stream generation,
token-block execution, DWH/hash search, scoring, CUDA, benchmarks, website expansion,
method-status upgrades, or solve claims.
