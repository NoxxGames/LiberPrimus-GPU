# Stage 5G shift_score CUDA Parity Reporting Development Log

## Scope

Stage 5G adds parity-reporting records, a CUDA device-code subset audit, solved-fixture-safe adapter preflight records, no-GPU-safe CLI commands, generated ignored reports, schemas, tests, docs, and consistency hooks.

## Implementation Notes

- Refactored CUDA-facing shift-score `.cu`/`.cuh` code to expose a POD/fixed-buffer ABI.
- Preserved the Stage 5F synthetic CUDA/native hash: `76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66`.
- Added `libreprimus cuda-parity-reporting` commands for parity report, device-code audit, solved-fixture-safe preflight, summary, validation, and summary display.
- Added committed Stage 5G YAML records under `data/cuda/`.
- Added ignored generated outputs under `experiments/results/cuda-parity-reporting/stage5g/`.

## Guardrails

- No new CUDA kernels.
- No solved-page or unsolved-page CUDA execution.
- No real Liber Primus data through CUDA.
- No GPU benchmark commands.
- No generated output publication.
- No website expansion.
- No canonical corpus activation.
- No page-boundary finalisation.
- No solve claim.

## Next Stage

Stage 5H - Gematria mod-29 shift_score contract and native parity fixture preparation.
