# Deep Research Bundle Workflow

Use the Stage 5AL export package, Stage 5AM static index metadata, Stage 5AN private content-pack metadata, and Stage 5AP token-block source-lock records as the private handoff layer for the next Deep Research prompt. They summarize Stage 5AI bundles, Stage 5AJ UsefulFiles metadata, Stage 5AK community-facts claim metadata, and page 49-51 token-block preflight records behind publication gates.

1. Start from `data/source-harvester/stage5ai-curated-research-bundle-summary.yaml`, `data/source-harvester/stage5aj-summary.yaml`, and `data/source-harvester/stage5ak-summary.yaml`.
2. Use `research-inputs/stage5ai/master_manifest.yaml` to identify bundle directories.
3. Prefer `source_cards.jsonl`, `content_index.jsonl`, and `deep_research_pack_index.json` over raw
   local source paths.
4. Preserve `do_not_assume_global.md`, `known_questions_global.md`, and per-bundle
   `do_not_assume.md` files as hard boundaries.
5. Treat generated extracts as private review inputs, not publishable content.

Do not use Google Drive as project storage. Do not publish generated bundle bodies, raw
`third_party/` material, raw Discord logs, images, PDFs, archives, audio/video, or extracted
payloads. Website expansion remains deferred to a future unnumbered project.

Stage 5AQ should evaluate exact page 49-51 token-to-value source locks, DWH context, and reliability from Stage 5AP token-block records, Stage 5AL metadata, Stage 5AM renderer records, Stage 5AN content-pack records, and private hosted content URLs. It should not execute experiments, run hash/preimage search, run LP-page OutGuess, run CUDA, benchmark, activate the canonical corpus, finalise page boundaries, or make solve claims.

Stage 5AJ adds extraction-fidelity and redaction policy: private handoffs should preserve runes, numbers, hashes, formulas, table shape, cell coordinates, highlights, and technical links, while public website views remain review-gated. Stage 5AK adds community claim records, correction logs, and arithmetic preflight metadata; those records are review inputs only, not source truth or solve evidence. Stage 5AL adds the website-ingest contract and publication gates that future Deep Research and website tools must cite. Stage 5AM adds an ignored private static index that is useful for navigation but remains generated output, not publication approval. Stage 5AN adds an ignored private content library and combined upload root, still generated output and still not publication approval. Stage 5AP adds token-block source-lock metadata and OutGuess controls that remain review/preflight records, not decoded text or execution permission.
