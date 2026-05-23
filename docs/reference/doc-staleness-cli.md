# Doc Staleness CLI

Stage 5AH extends `libreprimus consistency` with doc-staleness coverage commands.

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-doc-staleness `
  --source-of-truth data/project-state/stage5ah-doc-staleness-source-of-truth.yaml `
  --strict

.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-stage-ledger-staleness `
  --expected-latest-stage "Stage 5AH" `
  --expected-next-stage "Stage 5AI"

.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-operational-file-map-coverage

.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-current-next-stage-consistency `
  --expected-latest-stage "Stage 5AH" `
  --expected-next-stage "Stage 5AI"
```

Validation:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli consistency validate-stage5ah-doc-staleness `
  --source-of-truth data/project-state/stage5ah-doc-staleness-source-of-truth.yaml `
  --findings data/project-state/stage5ah-doc-staleness-findings.yaml `
  --stage-ledger-coverage data/project-state/stage5ah-stage-ledger-coverage.yaml `
  --operational-file-map-coverage data/project-state/stage5ah-operational-file-map-coverage.yaml `
  --next-stage-decision data/project-state/stage5ah-next-stage-decision.yaml `
  --summary data/project-state/stage5ah-doc-staleness-summary.yaml `
  --results-dir experiments/results/doc-staleness/stage5ah
```

Reports written with `--out` are generated outputs. Do not commit report bodies, local handoffs, raw source material, generated extraction bodies, SQLite files, or `codex-output/**`.
