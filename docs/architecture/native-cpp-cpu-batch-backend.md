# Native C++ CPU Batch Backend

Stage 5D adds a native C++20 CPU backend as a deterministic execution plane for future parity work.
It is not CUDA implementation and it does not replace Python orchestration.

The backend currently runs a small synthetic shift fixture through fixed candidate slots. It records
backend capability, threading parity, native/Python parity, and diagnostic metadata. The committed
records live under `data/native-cpu/`; generated JSON reports live under
`experiments/results/native-cpu/stage5d/` and remain ignored.

## Boundary

- `src/native_cpu/` owns native CPU-only execution helpers.
- `python/libreprimus/native_cpu/` owns orchestration, validation, export, and reporting.
- C++ must not launch Python worker scripts.
- Python remains the policy, manifest, and provenance control plane.
- CUDA source, CUDA kernels, GPU benchmarks, speedup claims, raw-data processing, website expansion,
  canonical corpus activation, page-boundary finalisation, and solve claims remain out of scope.

## Parity Role

Stage 5D gives future CUDA stages a native CPU baseline in addition to the Python CPU batch
reference. Stage 5E cites that baseline when selecting the `shift_score_kernel` contract, and
Stage 5F preserves it for the synthetic CUDA parity kernel. Future
CUDA kernel work must cite the Stage 5D native output hash, threading parity
records, and native/Python parity record before selecting an adapter for implementation.

Stage 5G adds a reporting layer over the Stage 5F synthetic hash and records blockers for
solved-fixture-safe adapter work. Stage 5H prepares the Gematria mod-29 native fixture contract and
records a separate synthetic numeric fixture hash. Future CUDA work must not treat the Stage 5D
uppercase Latin hash as the Gematria fixture hash.
