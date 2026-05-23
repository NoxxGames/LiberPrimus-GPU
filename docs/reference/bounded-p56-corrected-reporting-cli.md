# Bounded P56 Corrected Reporting CLI

Stage 5AE adds:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli corrected-bounded-p56-reporting build-formula-parity-report --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli corrected-bounded-p56-reporting build-reference-contract-repair --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli corrected-bounded-p56-reporting build-hash-material-policy --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli corrected-bounded-p56-reporting build-summary --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli corrected-bounded-p56-reporting validate-stage5ae
.\.venv\Scripts\python.exe -m libreprimus.cli corrected-bounded-p56-reporting summary
```

The CLI has no CUDA execution path, no full-p56 execution path, no unsolved-page path, no benchmark path, and no scored-experiment path. It writes compact YAML records and ignored JSON reports only.
