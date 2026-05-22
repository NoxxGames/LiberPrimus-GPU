# Prime-Minus-One CUDA Synthetic CLI

Command group:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic --help
```

Stage 5AA command sequence:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic build-kernel-implementation-records --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic build-run-records --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic run-synthetic-cuda-parity --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic build-parity-records --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic build-device-subset-audit --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic build-result-store-preflight --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic build-p56-blocker --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic build-scored-experiment-deferral --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic build-next-stage-decision --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic build-summary --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-cuda-synthetic validate-stage5aa
```

Use `--skip-cuda` for raw-data-free no-GPU validation paths. A skipped CUDA run must not select Stage 5AB.
