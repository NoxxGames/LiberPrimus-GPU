# Bounded P56 CUDA Parity CLI

The Stage 5AD CLI group is:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli bounded-p56-cuda-parity --help
```

Important commands:

- `build-run-records`
- `run-bounded-p56-cuda`
- `build-parity-records`
- `build-result-store-preflight`
- `build-score-summary-preflight`
- `build-full-p56-blocker`
- `build-scored-experiment-deferral`
- `build-doc-staleness-validation`
- `build-device-subset-audit`
- `build-next-stage-decision`
- `build-summary`
- `validate-stage5ad`
- `summary`

`run-bounded-p56-cuda` has a `--skip-cuda` mode for no-GPU CI-compatible validation. Local CUDA execution is bounded to `stage5z-validation-p56-bounded-v0`; full p56, unsolved-page CUDA, benchmarks, scored experiments, and generated-body publication remain blocked.
