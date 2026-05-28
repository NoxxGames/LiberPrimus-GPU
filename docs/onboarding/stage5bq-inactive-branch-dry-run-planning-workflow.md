# Stage 5BQ Inactive-Branch Dry-Run Planning Workflow

Use this workflow when reviewing the Stage 5BQ inactive-branch planning integration.

Start with committed metadata:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5bq
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5bq-summary
```

Read:

- `data/project-state/stage5bq-stage5bp-findings-integration.yaml`
- `data/token-block/stage5bq-string4-inactive-branch-planning-context.yaml`
- `data/token-block/stage5bq-errata-aware-dry-run-constraint-update.yaml`
- `data/token-block/stage5bq-string4-no-active-ingestion-proof.yaml`
- `data/token-block/stage5bq-future-dry-run-requirements.yaml`
- `data/token-block/stage5bq-stage5bd-dry-run-lineage-preservation.yaml`
- `data/project-state/stage5bq-summary.yaml`
- `data/project-state/stage5bq-next-stage-decision.yaml`

Interpretation boundary:

- Stage 5BP findings are integrated as `accept_with_warnings` metadata.
- String 4 remains `inactive_branch_context_only`.
- String 4 active input and dry-run ingestion are both false.
- The operator-errata sidecar is inactive planning metadata only.
- Stage 5AP, Stage 5AW, Stage 5AY, Stage 5AZ, Stage 5BB, and Stage 5BD active records remain unchanged.
- Byte-stream generation, branch materialisation, DWH/hash search, decoding, scoring, CUDA, benchmarking, website expansion, and solve claims remain blocked.

Do not use ignored Deep Research bodies, review-pack bodies, raw iddqd-v2/archive/Fandom/spreadsheet material, generated diagnostics, local completion summaries, full String 4 bodies, decoded bytes, or reconstructed streams as source truth.
