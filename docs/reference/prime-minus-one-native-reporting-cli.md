# Prime-Minus-One Native Reporting CLI

The Stage 5Y CLI group is:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-native-reporting --help
```

Primary commands:

- `build-parity-report`
- `build-result-store-integration`
- `build-score-summary-integration`
- `build-method-status-impact`
- `build-generated-body-policy`
- `build-full-p56-blocker-preservation`
- `build-cuda-contract-readiness-gate`
- `build-scored-experiment-readiness`
- `build-guardrails`
- `build-next-stage-decision`
- `build-summary`
- `validate-stage5y`
- `summary`

All commands are metadata/reporting commands. They must not be used to execute native parity, CUDA, CMake, GPU benchmarks, full p56, raw data, or unsolved pages.
