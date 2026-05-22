# Native Candidate Batch ABI CLI

Stage 5V adds:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli native-candidate-batch-conformance --help
```

## Build Commands

- `build-adapter-records`
- `build-conformance-fixtures`
- `run-native-conformance`
- `build-token-buffer-conformance`
- `build-schedule-conformance`
- `build-score-vector-conformance`
- `build-topk-conformance`
- `build-result-store-conformance`
- `build-implementation-status`
- `build-next-stage-decision`
- `build-summary`

## Validation

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli native-candidate-batch-conformance validate-stage5v `
  --adapter-records data/cuda/stage5v-native-candidate-batch-adapter.yaml `
  --conformance-fixtures data/cuda/stage5v-candidate-batch-conformance-fixtures.yaml `
  --token-buffer-conformance data/cuda/stage5v-token-buffer-conformance.yaml `
  --schedule-conformance data/cuda/stage5v-schedule-conformance.yaml `
  --score-vector-conformance data/cuda/stage5v-score-vector-conformance.yaml `
  --topk-conformance data/cuda/stage5v-topk-conformance.yaml `
  --result-store-conformance data/cuda/stage5v-native-conformance-result-store.yaml `
  --implementation-status data/cuda/stage5v-abi-implementation-status.yaml `
  --next-stage-decision data/cuda/stage5v-next-stage-decision.yaml `
  --summary data/cuda/stage5v-native-candidate-batch-conformance-summary.yaml `
  --results-dir experiments/results/cuda-candidate-batch-abi-conformance/stage5v
```

## Rules

The CLI is no-GPU-safe. It does not run CUDA, modify CUDA source, add kernels, run native/CUDA CMake, benchmark, process raw data, publish generated bodies, or make solve claims.
