# Token-Block Source-Lock Workflow

Use this workflow when a future stage works with the page 49-51 token block.

1. Read `STATUS.md`, `docs/roadmap/staged-plan.md`, and `data/project-state/stage5ap-summary.yaml`.
2. Inspect the committed Stage 5AP records under `data/token-block/` and `data/stego/`, then inspect the Stage 5AR coordinate records under `data/token-block/stage5ar-*`, the Stage 5AT review-pack records under `data/token-block/stage5at-*`, the Stage 5AU review-pack v2 records under `data/token-block/stage5au-*`, and the Stage 5AV decision/branch records under `data/token-block/stage5av-*`.
3. Treat the 32x8 token grid as a source-lock candidate, not decoded text.
4. Keep raw page images ignored and uncommitted.
5. Record any alternate alphabet order, source transcript, or DWH context explicitly.
6. Use null controls before interpreting any pattern.
7. Do not run OutGuess against LP pages unless a later explicit stage scopes assets, expected outputs, and toolchain readiness.

Generated Stage 5AP reports live under `experiments/results/token-block/stage5ap/` and `experiments/results/stego-controls/stage5ap/`; generated Stage 5AR coordinate reports live under `experiments/results/token-block/stage5ar/`; generated Stage 5AT review-pack reports live under `experiments/results/token-block/stage5at/` and `human-review-packs/stage5at/token-case-review/`; generated Stage 5AU v2 reports live under `experiments/results/token-block/stage5au/` and `human-review-packs/stage5au/token-case-review-v2/`; generated Stage 5AV decision reports live under `experiments/results/token-block/stage5av/`. They remain ignored except README/.gitkeep scaffolds.
