# Scoring Calibration CLI

The `libreprimus scoring` command group manages Stage 3C calibration.

## calibrate

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli scoring calibrate --stage3-results-dir experiments/results/bounded-auto-runs/stage3a --stage3b-results-dir experiments/results/bounded-auto-runs/stage3b --out-dir experiments/results/scoring-calibration/stage3c --allow-warnings
```

Writes ignored calibration JSON and JSONL outputs.

## crib-check

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli scoring crib-check --text "LIBER PRIMUS" --cribs data/scoring/cribs-tiny-v0.txt
```

Prints crib hits and `solve_claim=false`.

## calibration-summary

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli scoring calibration-summary --results-dir experiments/results/scoring-calibration/stage3c
```

Prints control counts, score ranges, Stage 3A/3B classifications, and the recommended next step.
