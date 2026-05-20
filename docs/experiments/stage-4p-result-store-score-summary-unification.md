# Stage 4P Result Store Score Summary Unification

Stage 4P is not a cryptanalytic experiment. It is a reporting stage that joins existing result and score surfaces into deterministic generated reports plus one committed aggregate summary.

## Commands

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli result-store build-source-inventory `
  --manifest experiments/manifests/result-store/stage4p-result-source-inventory.yaml `
  --out-dir experiments/results/result-store-unification/stage4p `
  --allow-warnings

.\.venv\Scripts\python.exe -m libreprimus.cli result-store unify-score-summaries `
  --manifest experiments/manifests/result-store/stage4p-score-summary-unification.yaml `
  --out-dir experiments/results/result-store-unification/stage4p `
  --allow-warnings

.\.venv\Scripts\python.exe -m libreprimus.cli result-store build-cross-stage-report `
  --manifest experiments/manifests/result-store/stage4p-cross-stage-report.yaml `
  --out-dir experiments/results/result-store-unification/stage4p `
  --summary-out data/research/stage4p-result-store-score-summary-unification-summary.yaml `
  --allow-warnings
```

Validate the local generated reports and committed summary:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli result-store validate-stage4p `
  --results-dir experiments/results/result-store-unification/stage4p `
  --summary data/research/stage4p-result-store-score-summary-unification-summary.yaml
```

Generated JSON, JSONL, and SQLite files under `experiments/results/result-store-unification/stage4p/` remain ignored and must not be staged.

