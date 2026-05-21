# Gematria Solved-Fixture CUDA Reporting CLI

CLI group: `libreprimus gematria-solved-fixture-cuda-reporting`

Commands:

- `build-parity-report`
- `build-controlled-expansion-gate`
- `build-boundary-review`
- `build-result-store-preflight`
- `build-no-unsolved-guardrail`
- `build-summary`
- `validate-stage5n`
- `summary`

The commands are raw-data-free and no-GPU-safe. They read committed Stage 5M and Stage 4P records and write compact Stage 5N YAML summaries plus ignored JSON reports. They do not run CUDA.
