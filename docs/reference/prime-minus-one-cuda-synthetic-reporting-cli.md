# Prime-Minus-One CUDA Synthetic Reporting CLI

Command group:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting --help
```

Common build sequence:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-parity-report --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-result-store-integration --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-score-summary-integration --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-method-status-impact --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-generated-body-policy --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-doc-staleness-validation --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-bounded-p56-preflight --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-full-p56-blocker --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-scored-experiment-deferral --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-next-stage-decision --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting build-summary --allow-warnings
```

Validation:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic-reporting validate-stage5ac
```

The command group has no CUDA execution path, no native execution path, no p56 execution path, no benchmark execution path, and no scored-experiment execution path.
