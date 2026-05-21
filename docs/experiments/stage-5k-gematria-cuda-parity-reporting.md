# Stage 5K Gematria CUDA Parity Reporting

Stage 5K is a reporting and preflight stage. It consumes committed Stage 5J/5H/4O/4I records, writes durable Stage 5K metadata, and generates ignored reports.

It does not:

- add or modify CUDA kernels
- execute CUDA
- process solved fixtures, unsolved pages, or real Liber Primus data through CUDA
- benchmark GPU performance
- make speedup or solve claims

Primary command sequence:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-parity-reporting build-parity-report --manifest experiments/manifests/cuda/stage5k-gematria-cuda-parity-reporting.yaml --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-parity-reporting audit-device-code --manifest experiments/manifests/cuda/stage5k-gematria-device-code-audit.yaml --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-parity-reporting build-solved-fixture-preflight --manifest experiments/manifests/cuda/stage5k-solved-fixture-safe-preflight.yaml --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-parity-reporting build-score-summary-preflight --manifest experiments/manifests/cuda/stage5k-solved-fixture-safe-preflight.yaml --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-parity-reporting build-summary --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-parity-reporting validate-stage5k
```

The selected next stage is Stage 5L solved-fixture-safe Gematria shift_score token mapping and native parity fixture preparation because solved-fixture-safe blockers remain.
