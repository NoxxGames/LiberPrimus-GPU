# Source Harvester Local Inventory CLI

Stage 5AG extends `libreprimus source-harvester` with local inventory commands.

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester inventory-local-sources `
  --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml `
  --source-root third_party `
  --results-dir experiments/results/source-harvester-local/stage5ag
```

Follow with `link-local-sources`, `build-source-lock-candidates`, `build-bundle-readiness`, `build-stage5ag-guardrail`, `build-stage5ag-next-stage-decision`, `build-stage5ag-summary`, and `validate-stage5ag`.

Validation:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester validate-stage5ag `
  --root-inventory data/source-harvester/stage5ag-local-source-root-inventory.yaml `
  --file-summary data/source-harvester/stage5ag-local-source-file-inventory-summary.yaml `
  --archive-summary data/source-harvester/stage5ag-local-archive-inventory-summary.yaml `
  --hash-summary data/source-harvester/stage5ag-local-source-hash-inventory-summary.yaml `
  --local-linkage data/source-harvester/stage5ag-manifest-local-linkage.yaml `
  --candidate-summary data/source-harvester/stage5ag-source-lock-candidate-summary.yaml `
  --gap-report data/source-harvester/stage5ag-local-source-gap-report.yaml `
  --bundle-readiness data/source-harvester/stage5ag-research-bundle-readiness.yaml `
  --guardrail data/source-harvester/stage5ag-local-source-guardrail.yaml `
  --next-stage-decision data/source-harvester/stage5ag-source-harvester-next-stage-decision.yaml `
  --summary data/source-harvester/stage5ag-source-harvester-summary.yaml `
  --results-dir experiments/results/source-harvester-local/stage5ag
```

These commands are local-only. They do not require `--allow-network`, do not use Google Drive storage, and do not make source interpretation claims.
