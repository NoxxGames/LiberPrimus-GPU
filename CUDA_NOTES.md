# CUDA Notes

## Purpose

This file records CUDA policy for future acceleration work.

## Current CUDA Status

CUDA remains deferred after Stage 3V and during Stage 3W. Existing CUDA code is scaffold and smoke-test infrastructure only unless a future stage explicitly adds CPU-reference behavior, parity tests, and benchmark coverage.

Do not use CUDA for Discord processing, image interpretation, OutGuess regression, cookie/hash packs, or broad unsolved-page campaigns.

## RTX 4060 Ti Target

The expected GPU target is RTX 4060 Ti.

## Compute Capability 8.9

RTX 4060 Ti uses compute capability 8.9, represented as CUDA architecture `89` in CMake.

## CMake CUDA Architecture Setting

When CUDA is enabled for smoke/scaffold builds, `CMAKE_CUDA_ARCHITECTURES` defaults to `89` unless the user supplies another value.

## CPU Reference First

Every future CUDA transform must follow a CPU reference implementation. CPU behavior, scoring semantics, reset/advance policy, and output records must be stable before acceleration.

## Future First CUDA Target

The likely first serious CUDA target is a batch transform-and-score API for already-reviewed CPU transforms. Hash cracking, Discord processing, image stego fishing, OCR, AI/ML interpretation, and raw data processing are not CUDA targets.

## Parity Tests

Every CUDA kernel must have CPU/GPU parity tests before optimization. Parity tests must include known inputs, negative controls, edge cases, and deterministic output comparisons.

## No Fast-Math Default

Do not enable fast math by default. Cryptanalytic scoring must remain reproducible.

## Memory Layout Planned Later

Memory layouts will be chosen after CPU transform, batch, and scoring APIs are stable.

## Top-K Only Output Principle

GPU kernels should return compact top-k or score summaries instead of dumping huge candidate sets.

## Profiling Tools Planned Later

Nsight Systems and Nsight Compute remain future tools. Do not run long profiling jobs before CPU/GPU parity tests and a benchmark plan exist.
