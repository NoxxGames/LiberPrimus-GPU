# Observation Promotion CLI

Stage 4L adds:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli observation-promotion build `
  --out-dir experiments/results/observation-promotion/stage4l `
  --ledger-out data/observations/review/stage4l-reviewed-observation-promotion-ledger.yaml `
  --readiness-out data/observations/review/stage4l-observation-promotion-readiness-records.yaml `
  --blockers-out data/observations/review/stage4l-observation-promotion-blocker-records.yaml `
  --manifest-readiness-out data/observations/review/stage4l-manifest-readiness-records.yaml `
  --summary-out data/observations/review/stage4l-reviewed-observation-promotion-summary.yaml `
  --allow-warnings
```

Validation:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli observation-promotion validate `
  --ledger data/observations/review/stage4l-reviewed-observation-promotion-ledger.yaml `
  --readiness data/observations/review/stage4l-observation-promotion-readiness-records.yaml `
  --blockers data/observations/review/stage4l-observation-promotion-blocker-records.yaml `
  --manifest-readiness data/observations/review/stage4l-manifest-readiness-records.yaml `
  --summary data/observations/review/stage4l-reviewed-observation-promotion-summary.yaml
```

Summary:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli observation-promotion summary `
  --summary data/observations/review/stage4l-reviewed-observation-promotion-summary.yaml
```

The CLI reads committed metadata only and writes generated JSON reports under an
ignored result path.

Stage 4L follow-up intake includes the bigram/Fibonacci-421 community claim as a
blocked `numeric_frequency_pattern_claim`. The CLI does not regenerate a bigram
matrix or execute the future audit manifest.
