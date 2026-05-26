# Decision Parser Repair CLI

Stage 5AW extends `libreprimus token-block` with parser-repair commands:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli token-block audit-stage5aw-decision-parser
.\.venv\Scripts\python.exe -m libreprimus.cli token-block repair-stage5aw-decision-variants
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5aw-repaired-branch-manifest
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5aw-updates
.\.venv\Scripts\python.exe -m libreprimus.cli token-block build-stage5aw-summary
.\.venv\Scripts\python.exe -m libreprimus.cli token-block validate-stage5aw
```

The commands read the local ignored Stage 5AU v2 decision template when building records, but validation uses committed compact Stage 5AW metadata and does not require raw images or generated review-pack bodies.

Generated JSON reports stay ignored under `experiments/results/token-block/stage5aw/`. Commit only the compact YAML records, schemas, docs, and tests.
