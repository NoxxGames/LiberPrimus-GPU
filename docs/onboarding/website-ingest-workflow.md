# Website-Ingest Workflow

Use this workflow for Stage 5AL-style metadata handoffs.

1. Validate the current source-harvester stage records.
2. Build `data/website-ingest/stage5al/` from committed metadata.
3. Build the private Deep Research export under `research-inputs/stage5al/`.
4. Validate publication gates and confirm public website-ready remains zero.
5. Keep generated export files, generated reports, raw third-party files, and `codex-output/**`
   ignored.

Future website work must consume the committed data package and must not infer publication
permission from source-card presence alone. Publication gates are mandatory.
