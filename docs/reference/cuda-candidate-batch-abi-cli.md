# CUDA Candidate Batch ABI CLI

The `libreprimus cuda-candidate-batch-abi` CLI builds and validates Stage 5U contract records.

## Commands

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-candidate-batch-abi build-candidate-batch-abi --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-candidate-batch-abi build-token-buffer-contract --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-candidate-batch-abi build-transform-parameter-contract --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-candidate-batch-abi build-key-schedule-contract --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-candidate-batch-abi build-stream-schedule-contract --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-candidate-batch-abi build-score-vector-contract --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-candidate-batch-abi build-topk-output-contract --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-candidate-batch-abi build-backend-surface-contract --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-candidate-batch-abi build-result-store-compatibility --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-candidate-batch-abi build-gap-closure --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-candidate-batch-abi build-next-stage-decision --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-candidate-batch-abi build-summary --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-candidate-batch-abi validate-stage5u
.\.venv\Scripts\python.exe -m libreprimus.cli cuda-candidate-batch-abi summary
```

## Rules

The commands are no-GPU-safe and raw-data-free. They write committed YAML metadata under `data/cuda/` and ignored JSON reports under `experiments/results/cuda-candidate-batch-abi/stage5u/`.
