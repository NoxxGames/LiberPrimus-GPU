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
