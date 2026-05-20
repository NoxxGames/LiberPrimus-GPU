# Result Store CLI

## CLI Overview

Stage 2B adds the `libreprimus result-store` command group for result-store manifests, solved-baseline imports, validation, summaries, and smoke runs.

## validate-manifest

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli result-store validate-manifest --manifest experiments/manifests/result-store/stage2b-solved-baseline-import.yaml
```

Validates the result-store import manifest and confirms search, scoring, CUDA, canonical corpus activation, and page-boundary finalization are disabled.

## import-solved-baseline

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli result-store import-solved-baseline --manifest experiments/manifests/result-store/stage2b-solved-baseline-import.yaml --solved-baseline-results experiments/results/solved-baselines/stage2a --out-dir experiments/results/result-store/stage2b --replace --allow-warnings
```

Imports Stage 2A solved-baseline generated outputs into JSONL and SQLite result stores.

## validate

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli result-store validate --results-dir experiments/results/result-store/stage2b --sqlite experiments/results/result-store/stage2b/results.sqlite3
```

Validates JSONL records, SQLite tables, count agreement, generated-artifact flags, and false safety flags.

## summary

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli result-store summary --results-dir experiments/results/result-store/stage2b
```

Prints concise run counts, artifact counts, pass/fail counts, and safety flags.

## stage2b-smoke

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli result-store stage2b-smoke --solved-baseline-manifest experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml --result-store-manifest experiments/manifests/result-store/stage2b-solved-baseline-import.yaml --solved-baseline-out-dir experiments/results/solved-baselines/stage2a --result-store-out-dir experiments/results/result-store/stage2b --replace --allow-warnings
```

Ensures Stage 2A solved-baseline outputs exist, imports them into the result store, validates the outputs, and prints a concise summary.

## Stage 4P Unification Commands

Stage 4P adds read-only reporting commands while preserving the Stage 2B import commands:

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

Validate the generated reports and committed aggregate summary:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli result-store validate-stage4p `
  --results-dir experiments/results/result-store-unification/stage4p `
  --summary data/research/stage4p-result-store-score-summary-unification-summary.yaml
```

## Generated Outputs

Generated Stage 2B outputs live under `experiments/results/result-store/stage2b/`. Generated Stage 4P outputs live under `experiments/results/result-store-unification/stage4p/`. Both remain ignored by Git. SQLite files and sidecars must not be staged.

## Troubleshooting

If import fails because Stage 2A outputs are missing, run `solved-baseline stage2a-smoke` or use `result-store stage2b-smoke`. If validation fails on false flags, inspect the imported Stage 2A summary before rerunning with `--replace`.
