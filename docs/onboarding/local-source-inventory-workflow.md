# Local Source Inventory Workflow

Use this workflow for Stage 5AG-style local source inventory and Stage 5AI-style curated extraction preparation after the Stage 5AH doc-staleness gate is clean.

1. Put user-provided source files under an ignored local root, normally `third_party/`.
2. Confirm raw files are ignored with `git status --short third_party` and `git check-ignore -v`.
3. Run `libreprimus source-harvester inventory-local-sources`.
4. Link local paths to the Stage 5AF manifest with `link-local-sources`.
5. Build source-lock candidates, gap records, bundle readiness, guardrails, next-stage decision, and summary records.
6. Commit only compact metadata under `data/source-harvester/`, schemas, docs, tests, and source code.
7. Before curated extraction work, validate Stage 5AH doc-staleness records and confirm current docs name Stage 5AI as the next stage.

Do not use Google Drive as a project storage location. Google/Dropbox/Colab exports must be local ignored files. Do not commit raw archives, images, PDFs, HTML, DOCX, audio, video, extracted bodies, full generated inventories, generated research bundles, or `codex-output/**`.
