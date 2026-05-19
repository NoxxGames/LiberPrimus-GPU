# Scoring CLI

Stage 4I adds the `libreprimus scoring` command group.

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli scoring consolidate `
  --out-dir experiments/results/scoring-consolidation/stage4i `
  --data-dir data/scoring `
  --allow-warnings

.\.venv\Scripts\python.exe -m libreprimus.cli scoring validate --data-dir data/scoring

.\.venv\Scripts\python.exe -m libreprimus.cli scoring report --data-dir data/scoring

.\.venv\Scripts\python.exe -m libreprimus.cli scoring check-cpu-batch-compatibility `
  --cpu-batch-summary data/research/stage4h-cpu-batch-api-summary.yaml `
  --data-dir data/scoring `
  --allow-warnings
```

The CLI writes committed scoring records under `data/scoring/` and generated reports under ignored `experiments/results/scoring-consolidation/stage4i/`.
