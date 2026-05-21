# Gematria Solved-Fixture Repeat CLI

The Stage 5O CLI group is:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-solved-fixture-cuda-repeat --help
```

Main commands:

- `build-repeat-run-records`
- `run-repeat-verification`
- `build-repeat-parity-records`
- `build-result-store-preflight`
- `build-score-summary-preflight`
- `build-expansion-decision`
- `build-summary`
- `validate-stage5o`
- `summary`

CI and no-GPU validation paths should use `run-repeat-verification --skip-run`. Local CUDA repeat
verification may omit `--skip-run`, but it must remain limited to the exact Stage 5M solved-fixture
buffers.
