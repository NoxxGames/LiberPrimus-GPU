# CUDA Solved-Family Readiness CLI

The `libreprimus cuda-solved-family-readiness` CLI builds and validates Stage 5T metadata records. It is raw-data-free and no-GPU-safe by default.

## Commands

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-solved-family-readiness build-solved-family-inventory --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-solved-family-readiness build-parity-matrix --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-solved-family-readiness build-kernel-readiness --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-solved-family-readiness build-batch-abi-gaps --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-solved-family-readiness build-benchmark-readiness --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-solved-family-readiness build-no-unsolved-guardrail --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-solved-family-readiness build-next-stage-decision --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-solved-family-readiness build-summary --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-solved-family-readiness validate-stage5t
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-solved-family-readiness summary
```

The commands write committed YAML records under `data/cuda/` and ignored JSON reports under `experiments/results/cuda-solved-family-readiness/stage5t/`.

## Rules

- No command runs CUDA.
- No command runs a benchmark.
- No command reads raw Liber Primus data.
- Validation rejects records that set solve, CUDA-execution, CUDA-source-change, benchmark, generated-output-publication, or unsolved-page flags.
