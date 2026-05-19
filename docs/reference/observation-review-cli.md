# Observation Review CLI

Stage 4J adds `libreprimus observation-review`.

Build committed review records and ignored local reports:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli observation-review build `
  --out-dir experiments/results/observation-review/stage4j `
  --policy-out data/observations/review/stage4j-observation-review-policy.yaml `
  --decisions-out data/observations/review/stage4j-observation-review-decisions.yaml `
  --promotions-out data/observations/review/stage4j-observation-promotion-records.yaml `
  --quarantine-out data/observations/review/stage4j-observation-quarantine-records.yaml `
  --summary-out data/observations/review/stage4j-observation-review-summary.yaml `
  --allow-warnings
```

Validate:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli observation-review validate `
  --policy data/observations/review/stage4j-observation-review-policy.yaml `
  --decisions data/observations/review/stage4j-observation-review-decisions.yaml `
  --promotions data/observations/review/stage4j-observation-promotion-records.yaml `
  --quarantine data/observations/review/stage4j-observation-quarantine-records.yaml `
  --summary data/observations/review/stage4j-observation-review-summary.yaml
```

Check operational docs and records for stale current-stage text or absolute
local paths:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli observation-review check-paths --repo-root .
```
