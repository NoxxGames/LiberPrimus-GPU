# Stage 4B Source-Lock CLI

The Stage 4B command group is:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-lock-triage --help
```

## Run

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-lock-triage run `
  --stage4a-dir experiments/results/discord-full-review/stage4a `
  --out-dir experiments/results/source-lock-triage/stage4b `
  --promoted-sources-out data/observations/archive/stage4b-promoted-source-records.yaml `
  --source-health-out data/locks/third-party/stage4b-source-health-records.yaml `
  --visual-observations-out data/observations/visual/stage4b-visual-observation-records.yaml `
  --negative-controls-out data/observations/research/stage4b-negative-control-records.yaml `
  --cookie-source-records-out data/observations/web/stage4b-cookie-candidate-source-records.yaml `
  --manifest-out-dir experiments/manifests/stage4b-disabled `
  --allow-warnings
```

`run` reads Stage 4A generated indexes if present and writes committed YAML records plus ignored diagnostics.

## Validate

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-lock-triage validate `
  --promoted-sources data/observations/archive/stage4b-promoted-source-records.yaml `
  --source-health data/locks/third-party/stage4b-source-health-records.yaml `
  --visual-observations data/observations/visual/stage4b-visual-observation-records.yaml `
  --negative-controls data/observations/research/stage4b-negative-control-records.yaml `
  --cookie-source-records data/observations/web/stage4b-cookie-candidate-source-records.yaml `
  --manifest-dir experiments/manifests/stage4b-disabled
```

Validation enforces false source-truth flags, no solve claims, disabled manifest flags, unsafe/private link handling, and review-only visual observation status.

## Summary

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-lock-triage summary `
  --promoted-sources data/observations/archive/stage4b-promoted-source-records.yaml `
  --visual-observations data/observations/visual/stage4b-visual-observation-records.yaml `
  --negative-controls data/observations/research/stage4b-negative-control-records.yaml `
  --manifest-dir experiments/manifests/stage4b-disabled
```
