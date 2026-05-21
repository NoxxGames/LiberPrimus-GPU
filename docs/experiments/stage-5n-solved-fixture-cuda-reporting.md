# Stage 5N Solved-Fixture CUDA Reporting

Stage 5N is reporting and planning infrastructure. It reports Stage 5M parity records, writes boundary-review records, records no-unsolved guardrails, and prepares result-store/score-summary preflight metadata.

Commands:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-cuda-reporting build-parity-report --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-cuda-reporting build-controlled-expansion-gate --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-cuda-reporting build-boundary-review --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-cuda-reporting build-result-store-preflight --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-cuda-reporting build-no-unsolved-guardrail --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-cuda-reporting build-summary --allow-warnings
```

Generated JSON reports are ignored under `experiments/results/gematria-solved-fixture-cuda-reporting/stage5n/`.
