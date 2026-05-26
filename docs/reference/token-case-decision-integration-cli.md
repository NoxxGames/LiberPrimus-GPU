# Token Case Decision Integration CLI

Stage 5AV adds local decision-integration commands under `libreprimus token-block`.

Typical local sequence:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block ingest-stage5av-decisions --decision-file human-review-packs/stage5au/token-case-review-v2/decision-template.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5av-decisions
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5av-decision-records --decision-file human-review-packs/stage5au/token-case-review-v2/decision-template.yaml
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5av-variant-branch-manifest
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5av-updates
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5av-summary
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5av
```

`validate-stage5av` is CI-safe because it validates committed compact records and does not require the ignored decision template or generated reports.
