# Gematria CUDA Parity Reporting CLI

Command group:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-parity-reporting --help
```

Commands:

- `build-parity-report`: converts Stage 5J synthetic parity metadata into Stage 5K parity records.
- `audit-device-code`: scans CUDA-facing `.cu` and `.cuh` files for conservative CUDA-C subset violations.
- `build-solved-fixture-preflight`: records solved-fixture-safe blockers without CUDA execution.
- `build-score-summary-preflight`: records Stage 4I score-summary requirements for future CUDA output.
- `build-summary`: writes the aggregate Stage 5K summary.
- `validate-stage5k`: validates committed records and generated summary parity.
- `summary`: prints the committed summary.

The command group is no-GPU-safe by default. It does not execute CUDA, read raw data, or require a local CUDA toolkit.
