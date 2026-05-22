# Prime-Minus-One Native Parity CLI

The Stage 5X command group is:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli prime-minus-one-native-parity --help
```

Primary commands:

- `build-run-records`
- `run-native-parity`
- `build-parity-records`
- `build-result-store-preflight`
- `build-score-summary-preflight`
- `build-full-p56-blocker`
- `build-guardrails`
- `build-next-stage-decision`
- `build-summary`
- `validate-stage5x`
- `summary`

The build commands write committed YAML metadata under `data/cuda/` and ignored JSON/JSONL reports under `experiments/results/prime-minus-one-native-parity/stage5x/`.

The CLI does not run CUDA, native C++ CMake, GPU benchmarks, full p56 parity, unsolved-page inputs, or generated-body publication.
