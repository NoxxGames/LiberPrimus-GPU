# Onion 7 Seed Pack CLI

Stage 3S adds the `post-discord` CLI group for the Onion 7 explicit seed-pack manifest.

## Validate Manifest

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord validate-manifest `
  --manifest experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml
```

Validation checks the experiment ID, candidate cap, CPU-only policy, disabled CUDA, no-solve flags, and expected candidate count. It does not execute the experiment.

## Run

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord run-onion7-seed-pack `
  --manifest experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml `
  --out-dir experiments/results/post-discord/stage3s `
  --top-k 25 `
  --allow-warnings
```

The command executes only `EXP-3R-003`. It writes candidate records, top candidates, summary JSON, warnings, and calibrated score details to ignored output paths.

## Summary

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord summary `
  --results-dir experiments/results/post-discord/stage3s
```

The summary prints counts and top-candidate metadata only.

## Safety

The CLI does not read raw Discord logs or raw page images. It does not run CUDA, broad route searches, arbitrary number tables, or solve-claim logic.
