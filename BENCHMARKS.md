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
