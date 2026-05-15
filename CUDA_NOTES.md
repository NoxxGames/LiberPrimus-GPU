# CUDA Notes

## Purpose

This file records CUDA policy for future acceleration work.

## CUDA status in Stage 0A

CUDA is optional in Stage 0A and limited to a guarded smoke kernel.

## RTX 4060 Ti target

The expected GPU target is RTX 4060 Ti.

## Compute capability 8.9

RTX 4060 Ti uses compute capability 8.9, represented as CUDA architecture `89` in CMake.

## CMake CUDA architecture setting

When CUDA is enabled, `CMAKE_CUDA_ARCHITECTURES` defaults to `89` unless the user supplies another value.

## CPU reference first

Every future CUDA transform must follow a CPU reference implementation.

## Parity tests

Every CUDA kernel must have CPU/GPU parity tests before optimization.

## No fast-math default

Do not enable fast math by default. Cryptanalytic scoring must remain reproducible.

## Memory layout planned later

Memory layouts will be chosen after the CPU transform and scoring APIs are stable.

## Top-k only output principle

GPU kernels should return compact top-k or score summaries instead of dumping huge candidate sets.

## Profiling tools planned later

Nsight Systems and Nsight Compute are planned for later stages. Do not run long profiling jobs in Stage 0A.
