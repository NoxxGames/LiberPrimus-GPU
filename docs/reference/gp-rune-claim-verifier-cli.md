# GP/Rune Claim Verifier CLI

Stage 3T extends the `post-discord` CLI group for `EXP-3R-004`.

## Validate Manifest

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord validate-gp-rune-manifest `
  --manifest experiments/manifests/post-discord/EXP-3R-004-gp-rune-claim-verifier-a.yaml
```

Validation checks the experiment ID, claim cap, CPU-only policy, disabled CUDA, and no-solve flags. It does not execute verification.

## Run Verifier

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord run-gp-rune-verifier `
  --manifest experiments/manifests/post-discord/EXP-3R-004-gp-rune-claim-verifier-a.yaml `
  --promoted-observations data/observations/discord/stage3r-promoted-observation-records.yaml `
  --visual-observations data/observations/visual/visual-numeric-observations-v0.yaml `
  --out-dir experiments/results/post-discord/stage3t `
  --allow-warnings
```

The command executes only `EXP-3R-004` and writes ignored verification outputs.

## Summary

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli post-discord gp-rune-summary `
  --results-dir experiments/results/post-discord/stage3t
```

## Safety

The verifier does not search neighbouring spans, process raw Discord logs, process page images, run CUDA, or claim a solve.
