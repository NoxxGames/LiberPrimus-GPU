# Stage 5D Native C++ CPU Batch Threading

## Scope

Stage 5D adds a native C++ CPU batch backend and deterministic threading baseline. The stage is
CPU-only infrastructure and preserves Python as orchestration.

Out of scope:

- CUDA kernels or CUDA transform execution.
- GPU benchmarks, speedup claims, or performance claims.
- Broad experiments, raw-data processing, website expansion, canonical corpus activation,
  page-boundary finalisation, and solve claims.

## Implementation Notes

- Added `src/native_cpu/` with deterministic synthetic batch execution and range partitioning.
- Added C++ tests for backend output determinism and thread range coverage.
- Added `python/libreprimus/native_cpu/` and `libreprimus native-cpu` CLI commands.
- Added Stage 5D schemas, manifests, committed YAML records, docs, tests, and consistency checks.
- Generated reports are written under `experiments/results/native-cpu/stage5d/` and remain ignored.

## Local Result

- Backend capability records: `1`
- Threading records: `5`
- Parity records: `1`
- Diagnostic records: `1`
- Thread counts: `1`, `2`, `4`, `8`, `16`
- Output hash: `76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66`
- Native/Python parity: `true`

## Next

Stage 5E should define the first CUDA kernel contract and CPU/native parity adapter selection while
keeping implementation, benchmarking, speedup claims, raw data, website expansion, and solve claims
blocked unless explicitly scoped.
