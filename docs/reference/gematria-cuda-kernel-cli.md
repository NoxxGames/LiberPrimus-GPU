# Gematria CUDA Kernel CLI

The Stage 5J CLI group is:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli gematria-cuda-kernel --help
```

Commands:

- `build-implementation-records`: writes committed implementation metadata and ignored reports.
- `attempt-build`: records optional local CUDA build status, or a no-GPU-safe skipped build.
- `run-synthetic-parity`: runs the synthetic CUDA parity executable only when the build passed.
- `build-summary`: writes the committed aggregate Stage 5J summary.
- `validate-stage5j`: validates implementation, build, parity, summary, and generated-output policy.
- `summary`: prints the committed Stage 5J summary.

The no-GPU-safe CI path uses `attempt-build --skip-build` and records skipped parity. Local CUDA
parity requires the optional CUDA build output and remains synthetic-only.
