# Document Staleness CLI

Run the Stage 5AB staleness check:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-doc-staleness `
  --source-of-truth data/project-state/stage5ab-doc-staleness-source-of-truth.yaml `
  --strict
```

Useful options:

- `--repo-root .` scans a specific checkout.
- `--format text|json|jsonl` changes output format.
- `--write-report experiments/results/doc-staleness/stage5ab/staleness_findings.json` writes generated ignored reports.
- `--strict` returns a non-zero exit code when findings exist.

The command reads `data/project-state/operational-file-map.yaml` when present. Missing optional generated outputs are not required. The command does not run CUDA, native code, benchmarks, experiments, or raw-data processing.
