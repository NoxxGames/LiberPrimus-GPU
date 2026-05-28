# Website-Ingest Workflow

Use this workflow for Stage 5AL-style metadata handoffs, Stage 5AM-style static metadata rendering, Stage 5AN-style private content-pack handoff, Stage 5AP token-block references, Stage 5AR coordinate-lock references, Stage 5AT review-pack references, Stage 5BI Fandom/source-lock references, and Stage 5BJ original/archive crosswalk references that need to remain metadata-only.

1. Validate the current source-harvester stage records.
2. Build `data/website-ingest/stage5al/` from committed metadata.
3. Build the private Deep Research export under `research-inputs/stage5al/`.
4. Validate publication gates and confirm public website-ready remains zero.
5. Render the optional private static index with `libreprimus website-render build-stage5am-site`.
6. Validate the static index with `libreprimus website-render validate-stage5am`.
7. Build and validate the private content pack and SFTP webroot with `libreprimus deep-research-export` when URL-based Deep Research handoff is needed.
8. Keep generated export files, generated reports, raw third-party files, static website files, private content-pack files, hosted private-content files, combined webroots, and `codex-output/**`
   ignored.

Future website work must consume the committed data package and must not infer publication
permission from source-card presence alone. Publication gates are mandatory, Stage 5AM renderer output under `website-export/stage5am/` remains a private generated artifact, Stage 5AN private content under `deep-research-content-packs/stage5an/` plus `website-export/stage5an/` remains private generated handoff material, and Stage 5AP token-block records plus Stage 5AR coordinate records plus Stage 5AT review-pack records plus Stage 5BI Fandom/source-lock records plus Stage 5BJ crosswalk closure records must not be rendered as decoded text, image interpretation, automatic transcription changes, original-media equivalence, experiment inputs, or solve evidence unless a later review changes that gate.
