# Gematria Shift Contract CLI

Stage 5H adds the `libreprimus gematria-shift-contract` command group.

## Build

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-shift-contract build-contract `
  --manifest experiments/manifests/cuda/stage5h-gematria-shift-score-contract.yaml `
  --out-dir experiments/results/gematria-shift-contract/stage5h `
  --contract-out data/cuda/stage5h-gematria-shift-score-contract.yaml `
  --allow-warnings
```

Use `build-native-fixtures`, `build-solved-fixture-mapping`, `build-score-summary-plan`, and
`build-summary` to regenerate the remaining records.

## Validate

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-shift-contract validate-stage5h `
  --contract data/cuda/stage5h-gematria-shift-score-contract.yaml `
  --fixtures data/cuda/stage5h-gematria-native-parity-fixtures.yaml `
  --mapping data/cuda/stage5h-gematria-solved-fixture-safe-mapping.yaml `
  --score-summary-plan data/cuda/stage5h-gematria-score-summary-parity-plan.yaml `
  --summary data/cuda/stage5h-gematria-shift-contract-summary.yaml `
  --results-dir experiments/results/gematria-shift-contract/stage5h
```

The CLI is no-GPU-safe and does not execute CUDA transforms.
