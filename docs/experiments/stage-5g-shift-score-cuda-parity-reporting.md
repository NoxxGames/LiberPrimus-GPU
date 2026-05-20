# Stage 5G shift_score CUDA Parity Reporting

Stage 5G is a reporting and preflight stage. It reads committed Stage 5F/5E/5D metadata, reports the synthetic CUDA/native hash match, audits CUDA-facing source style, and records blockers for future solved-fixture-safe adapter work.

## Inputs

- `data/cuda/stage5f-cuda-synthetic-kernel-summary.yaml`
- `data/cuda/stage5f-cuda-synthetic-parity-records.yaml`
- `data/cuda/stage5e-first-kernel-contract-summary.yaml`
- `data/native-cpu/stage5d-native-cpu-summary.yaml`
- Stage 5G manifests under `experiments/manifests/cuda/`

## Committed Outputs

- `data/cuda/stage5g-shift-score-parity-report.yaml`
- `data/cuda/stage5g-cuda-device-code-subset-audit.yaml`
- `data/cuda/stage5g-solved-fixture-safe-adapter-preflight.yaml`
- `data/cuda/stage5g-cuda-parity-reporting-summary.yaml`

## Ignored Outputs

Generated JSON reports remain ignored under `experiments/results/cuda-parity-reporting/stage5g/`.

## Guardrails

Stage 5G does not:

- add new CUDA kernels
- run solved pages through CUDA
- run unsolved pages through CUDA
- run GPU benchmark commands
- process real Liber Primus data
- publish generated outputs
- expand the website
- activate the canonical corpus
- finalise page boundaries
- make solve claims

The recommended next stage is Stage 5H: Gematria mod-29 `shift_score` contract and native parity fixture preparation.
