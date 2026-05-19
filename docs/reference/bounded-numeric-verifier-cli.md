# Bounded Numeric Verifier CLI

The Stage 4D CLI group is:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-numeric --help
```

## Run

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-numeric run `
  --manifest-dir experiments/manifests/stage4b-disabled `
  --stage4b-visual data/observations/visual/stage4b-visual-observation-records.yaml `
  --stage4c-tasks data/observations/visual/stage4c-visual-annotation-tasks.yaml `
  --stage4c-cuneiform data/observations/visual/stage4c-cuneiform-reading-candidates.yaml `
  --stage4c-dot data/observations/visual/stage4c-dot-pattern-annotation-tasks.yaml `
  --stage4c-delimiter data/observations/visual/stage4c-delimiter-annotation-tasks.yaml `
  --stage4c-negative data/observations/visual/stage4c-visual-negative-control-annotation-tasks.yaml `
  --out-dir experiments/results/bounded-numeric/stage4d `
  --allow-warnings
```

## Validate

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-numeric validate `
  --results-dir experiments/results/bounded-numeric/stage4d
```

## Summary

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-numeric summary `
  --results-dir experiments/results/bounded-numeric/stage4d
```

## Output Policy

The CLI writes generated JSON/JSONL outputs under `experiments/results/bounded-numeric/stage4d/`. These files are ignored and must not be committed.

The CLI keeps `solve_claim=false`, `cuda_used=false`, `trusted_as_canonical=false`, and `no_fudge_policy=true`.
