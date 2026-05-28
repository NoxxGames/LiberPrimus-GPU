# Stage 5BO Token-Case Human-Review Errata Workflow

Use this workflow when reviewing the Stage 5BO operator-errata integration.

Start with committed metadata:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5bo
.\.venv\Scripts\python.exe -m libreprimus.cli token-block stage5bo-summary
```

The original `decision-template.yaml` remains historical ignored input. The corrected `decision-template-corrected.yaml` is operator errata ignored input. Neither template body is committed.

Read:

- `data/token-block/stage5bo-decision-template-correction-source-lock.yaml`
- `data/token-block/stage5bo-token-case-human-review-errata.yaml`
- `data/token-block/stage5bo-errata-aware-token-option-universe.yaml`
- `data/token-block/stage5bo-string4-branch-membership-after-errata.yaml`
- `data/token-block/stage5bo-stage5bn-addendum-integration.yaml`
- `data/project-state/stage5bo-summary.yaml`

Interpretation boundary:

- The errata-aware option universe is inactive planning metadata only.
- String 4 full-branch status is not active ingestion.
- Canonical transcription is unchanged.
- Active Stage 5AW, Stage 5AY, Stage 5AZ, and Stage 5BD records remain unchanged.
- Byte-stream generation and execution remain blocked.

Do not use ignored review-pack bodies, full String 4 bodies, decoded bytes, raw iddqd-v2/archive/Fandom/spreadsheet material, generated diagnostics, or local completion summaries as source truth.
