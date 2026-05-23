# Deep Research Bundle Workflow

Use Stage 5AI bundles as the private handoff layer for the next Deep Research prompt.

1. Start from `data/source-harvester/stage5ai-curated-research-bundle-summary.yaml`.
2. Use `research-inputs/stage5ai/master_manifest.yaml` to identify bundle directories.
3. Prefer `source_cards.jsonl`, `content_index.jsonl`, and `deep_research_pack_index.json` over raw
   local source paths.
4. Preserve `do_not_assume_global.md`, `known_questions_global.md`, and per-bundle
   `do_not_assume.md` files as hard boundaries.
5. Treat generated extracts as private review inputs, not publishable content.

Do not use Google Drive as project storage. Do not publish generated bundle bodies, raw
`third_party/` material, raw Discord logs, images, PDFs, archives, audio/video, or extracted
payloads. Website expansion remains deferred to a future unnumbered project.

Stage 5AJ should evaluate source inventory and reliability from Stage 5AI metadata. It should not
execute experiments, run CUDA, benchmark, activate the canonical corpus, finalise page boundaries,
or make solve claims.
