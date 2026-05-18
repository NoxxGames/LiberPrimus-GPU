> This Wiki page mirrors $sourceRel. The repository tutorial file is the source of truth.

# Solved Baselines

## Purpose

Run known solved-page fixtures as regression checks, not solve claims.

## Commands

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli solved-fixture validate
.\.venv\Scripts\python.exe -m libreprimus.cli solved-baseline validate-manifest `
  --manifest experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml
```

## Expected Outputs

Validation should pass. Generated reproduction outputs, when produced, remain ignored.

## What Not To Commit

Do not commit generated solved-baseline output records or raw mirrored reference files.

## Troubleshooting

If real-source fixtures are unavailable locally, use raw-data-free validation paths and committed
fixtures only.
