# Gematria Expanded Solved-Fixture CUDA CLI

Stage 5R commands live under:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-expanded-solved-fixture-cuda --help
```

Main commands:

- `build-run-records`
- `run-cuda-parity`
- `build-parity-records`
- `build-boundary-records`
- `build-result-store-preflight`
- `build-score-summary-preflight`
- `build-summary`
- `validate-stage5r`
- `summary`

CI and no-GPU environments should use `run-cuda-parity --skip-run --allow-warnings`. A skipped run must not be recorded as a parity pass. Local CUDA execution is allowed only for the three Stage 5Q mapped direct-translation candidates and must not be used for benchmarking or unsolved-page data.
