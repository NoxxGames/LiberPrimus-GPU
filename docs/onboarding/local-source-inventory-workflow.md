# Local Source Inventory Workflow

Use this workflow for Stage 5AG-style local source inventory, Stage 5AI-style curated extraction metadata, and Stage 5AJ-style UsefulFilesAndIdeas metadata after the Stage 5AH doc-staleness gate is clean.

1. Put user-provided source files under an ignored local root, normally `third_party/`.
2. Confirm raw files are ignored with `git status --short third_party` and `git check-ignore -v`.
3. Run `libreprimus source-harvester inventory-local-sources`.
4. Link local paths to the Stage 5AF manifest with `link-local-sources`.
5. Build source-lock candidates, gap records, bundle readiness, guardrails, next-stage decision, and summary records.
6. Commit only compact metadata under `data/source-harvester/`, schemas, docs, tests, and source code.
7. Before Deep Research handoff work, validate Stage 5AI and Stage 5AJ records and confirm current docs name Stage 5AK as the next stage.

Do not use Google Drive as a project storage location. Google/Dropbox/Colab exports must be local ignored files. Do not commit raw archives, images, PDFs, HTML, DOCX, XLSX, audio, video, extracted bodies, full generated inventories, generated research bundles, or `codex-output/**`. Stage 5AI generated bundle bodies under `research-inputs/stage5ai/` and Stage 5AJ generated UsefulFiles bodies under `research-inputs/stage5aj/` are private/local inputs for Stage 5AK-style Deep Research review, not publication artefacts.
