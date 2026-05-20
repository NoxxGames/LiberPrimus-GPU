# Result Store Unification CLI

Stage 4P extends `libreprimus result-store` with read-only reporting commands.

## build-source-inventory

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli result-store build-source-inventory `
  --manifest experiments/manifests/result-store/stage4p-result-source-inventory.yaml `
  --out-dir experiments/results/result-store-unification/stage4p `
  --allow-warnings
```

Inventories committed summaries and optional ignored generated outputs. Missing optional generated outputs are warnings. Raw-required sources are skipped explicitly.

## unify-score-summaries

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli result-store unify-score-summaries `
  --manifest experiments/manifests/result-store/stage4p-score-summary-unification.yaml `
  --out-dir experiments/results/result-store-unification/stage4p `
  --allow-warnings
```

Writes unified result records and Stage 4I-compatible score-summary views. Unknown score semantics become `scoring_not_available`.

## build-cross-stage-report

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli result-store build-cross-stage-report `
  --manifest experiments/manifests/result-store/stage4p-cross-stage-report.yaml `
  --out-dir experiments/results/result-store-unification/stage4p `
  --summary-out data/research/stage4p-result-store-score-summary-unification-summary.yaml `
  --allow-warnings
```

Builds method-status joins, a cross-stage report, and the committed aggregate summary.

## validate-stage4p

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli result-store validate-stage4p `
  --results-dir experiments/results/result-store-unification/stage4p `
  --summary data/research/stage4p-result-store-score-summary-unification-summary.yaml
```

Validates generated Stage 4P reports and the committed summary against policy flags and schemas. This command does not require raw data.

