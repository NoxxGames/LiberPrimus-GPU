# Benchmarks

## Benchmark philosophy

Benchmarks should answer whether an implementation is useful, correct, and stable under pinned conditions.

## Stage 0A benchmark status

No performance benchmarks are implemented or run in Stage 0A.

## Future benchmark list

Future benchmarks may cover transform throughput, scorer throughput, CPU/GPU parity overhead, memory transfer cost, and top-k reduction cost.

## Regression thresholds

Regression thresholds should be set after a stable baseline exists.

## Hardware metadata

Benchmark output must include CPU, GPU, driver, CUDA toolkit, compiler, OS, clock policy where known, and power mode if relevant.

## CUDA benchmark rules

CUDA benchmarks require parity tests first and must avoid unbounded search or stress behavior by default.

## Stage 4Q CPU Benchmark Planning

Stage 4Q records benchmark planning and parity readiness only. It writes committed CPU benchmark plan and CUDA parity readiness metadata, plus ignored environment and CPU smoke diagnostics under `experiments/results/benchmarks/stage4q/`.

Stage 4Q CPU smoke timings are diagnostic only. They are not performance claims, speedup evidence, CUDA benchmarks, or authorization to implement GPU kernels.

Stage 5A uses Stage 4Q records for CUDA planning and parity scaffolding only. It records target plans, non-targets, parity scaffolds, and implementation gates without running GPU benchmarks or making speedup claims. Stage 5B records a CUDA parity harness skeleton, backend capability profiles, and future-kernel matrix rows without running GPU benchmarks or making speedup claims. Stage 5C records CUDA build profiles, toolchain detection, device detection, and optional smoke-build status without running GPU benchmarks or making speedup claims. Stage 5D records native C++ CPU backend diagnostics and threading parity without GPU benchmarks or speedup claims. Stage 5E records first-kernel contract selection without GPU benchmarks or speedup claims. Stage 5F synthetic-only parity implementation is next; website expansion is deferred to Stage 6.

## Stage 5C CUDA Build/Device Detection

Stage 5C device detection is hardware metadata, not a benchmark. Toolchain and device records may mention local CUDA availability and optional 16 GB hardware, but no local GPU profile is required by CI and no speedup claim is allowed.

## Stage 5D Native CPU Diagnostics

Stage 5D native CPU runtime values are diagnostic only. Matching one-thread and multi-thread output
hashes establish deterministic threading behavior for the synthetic fixture; they are not throughput
benchmarks, CPU optimization claims, GPU benchmarks, or speedup evidence.

## Stage 5E Kernel Contract Boundary

Stage 5E selected `shift_score_kernel` as a future contract only. It did not run a CUDA kernel,
GPU benchmark, profiler, or throughput comparison. Do not report Stage 5E records as speedup or
performance evidence.

## Do not run long benchmarks by default

Default test commands must remain short and safe.

## Stage 0D lightweight timing policy

Stage 0D records elapsed milliseconds for parsing, signature building, matching, boundary inference, and glyph-variant summarization. These values are for regression awareness only and are not benchmark claims. No GPU benchmark is required for transcript alignment.

## Public hardware tutorial policy

Public hardware tutorials must not imply speed claims without benchmark records, hardware metadata, source locks, and reproducible commands.

## Stage 0D-followup timing policy

Stage 0D-followup records elapsed milliseconds for transcript view construction, matching, gap analysis, and boundary audit. These timings are diagnostic metadata only. They are not benchmark claims and do not justify optimization work or CUDA changes.

## Stage 0E timing policy

Stage 0E records generation timings for profile validation, tokenization, page-candidate integration, and separator inventory. These values are diagnostics only and are not GPU benchmarks.

## Stage 1A timing policy

Stage 1A reproduction records elapsed milliseconds for fixture diagnostics only. These timings are not benchmark claims and do not involve CUDA.
## Stage 1B Timing Policy

Stage 1B reproduction timing is diagnostic only. It is not a GPU benchmark and must not be used to make hardware speed claims.

The fixture transforms are CPU-only, deterministic, and small. CUDA benchmarking remains out of scope.
## Stage 1C Timing Note

Stage 1C reproduction timing is diagnostic only. It is CPU-only fixture validation, not a GPU benchmark and not a performance claim.

## Stage 1D Timing Note

Stage 1D prime-stream reproduction timing is diagnostic only. Prime generation is deterministic and CPU-only for a small known fixture. It is not a GPU benchmark, speed claim, or optimization target.

## Stage 2A Timing Note

Stage 2A manifest-runner elapsed milliseconds are diagnostic metadata only. Registry dispatch is CPU-only and small; it is not a benchmark, speed claim, search throughput measurement, or CUDA readiness signal.

## Stage 2B Timing Note

Stage 2B result-store timings are diagnostic metadata for JSONL/SQLite import and validation only. They are not throughput benchmarks, search measurements, or CUDA readiness signals.
