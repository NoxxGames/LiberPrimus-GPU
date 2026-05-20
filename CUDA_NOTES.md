# CUDA Notes

## Purpose

This file records CUDA policy for future acceleration work.

## Current CUDA Status

CUDA remains deferred after Stage 5G except for the selected synthetic-only `shift_score_kernel` parity target and its reporting/audit metadata. Existing CUDA code is scaffold, smoke-test infrastructure, the Stage 5F synthetic fixture kernel, and Stage 5G conservative CUDA-C subset hardening only unless a future stage explicitly adds CPU-reference behavior, native CPU parity behavior, unified result-surface review, score-summary parity tests, benchmark-planning acceptance, Stage 5A planning-gate acceptance, Stage 5B harness acceptance, Stage 5C build/device readiness acceptance, Stage 5D deterministic threading acceptance, Stage 5E first-kernel contract acceptance, Stage 5F synthetic parity acceptance, Stage 5G device-code subset acceptance, and benchmark coverage.

Do not use CUDA for Discord processing, image interpretation, OutGuess regression, cookie/hash packs, or broad unsolved-page campaigns.

## RTX 4060 Ti Target

The expected GPU target is RTX 4060 Ti.

## Compute Capability 8.9

RTX 4060 Ti uses compute capability 8.9, represented as CUDA architecture `89` in CMake.

## CMake CUDA Architecture Setting

When CUDA is enabled for smoke/scaffold builds, `CMAKE_CUDA_ARCHITECTURES` defaults to `89` unless the user supplies another value. Stage 5C records build profile metadata only; the no-GPU CI profile must remain valid and the local 16 GB profile is optional.

## CPU Reference First

Every future CUDA transform must follow a CPU reference implementation. Stage 4H makes `libreprimus.cpu_batch` the current CPU batch parity contract, Stage 4I makes score-summary records the current scoring contract, Stage 4M keeps image/bigram observations out of CUDA scope until reproducible controls exist, Stage 4N keeps stego/audio positive-control readiness out of CUDA scope until fixtures, expected outputs, and toolchains are ready, Stage 4O records deterministic CPU batch parity expectations for expanded adapters, Stage 4P makes result-store and score-summary surfaces comparable, Stage 4Q records benchmark/parity planning gates, Stage 5A records target plans, non-targets, parity scaffolds, and implementation gates, Stage 5B records harness plans, parity fixtures, backend capability profiles, and future-kernel matrix rows, Stage 5C records CUDA build/device metadata, Stage 5D records native C++ CPU threading parity, Stage 5E selects the first future kernel contract, Stage 5F records synthetic parity for that contract, and Stage 5G records parity reporting plus conservative device-code subset compliance. CPU behavior, scoring semantics, reset/advance policy, review state, output records, unified result surfaces, parity expectations, benchmark scope, Stage 5A planning gates, Stage 5B harness records, Stage 5C build/device records, Stage 5D native output hashes, Stage 5E contract records, Stage 5F synthetic parity records, and Stage 5G reporting/audit records must be stable before acceleration.

## Future First CUDA Target

The selected first CUDA contract is `shift_score_kernel` for `caesar_mod29`, backed by the Stage 5E `native_cpu_synthetic_shift_adapter` mapping and Stage 5D native output hash. Stage 5F implements only that synthetic-only parity kernel over uppercase Latin A-Z fixture text and shifts, and Stage 5G reports the hash match while keeping solved-fixture CUDA blocked. It is still not broad CUDA implementation or production Gematria mod-29 behavior. Hash cracking, Discord processing, image stego fishing, audio/stego extraction, OCR, AI/ML interpretation, website expansion, and raw data processing are not CUDA targets.

## Parity Tests

Every CUDA kernel must have CPU/GPU parity tests before optimization. Parity tests must include known inputs, negative controls, edge cases, deterministic output comparisons, matching Stage 4H `output_text_hash` / `output_token_hash` records, Stage 4O parity expectation records for supported adapters, Stage 4P unified result surfaces for cross-stage score/status comparison, Stage 4Q parity readiness gates, Stage 5A target/scaffold/gate records, Stage 5B harness/fixture/backend/matrix records, Stage 5C build/device records, Stage 5D native CPU threading/parity records, Stage 5E first-kernel contract records, Stage 5F synthetic parity records, and Stage 5G parity-reporting/device-code audit records.

## CUDA-C Device-Code Subset

CUDA-facing `.cu` and `.cuh` paths must use a conservative CUDA-C style: POD structs, fixed-size arrays, raw pointers, explicit counts/capacities, explicit output buffers, and integer status codes. Do not use STL containers or strings, exceptions, RTTI, lambdas, dynamic allocation, or C++ ownership types in kernel/device-facing paths. Host-side C++ helpers belong outside the CUDA-facing ABI.

## No Fast-Math Default

Do not enable fast math by default. Cryptanalytic scoring must remain reproducible.

## Memory Layout Planned Later

Memory layouts will be chosen after CPU transform, batch, and scoring APIs are stable.

## Top-K Only Output Principle

GPU kernels should return compact top-k or score summaries instead of dumping huge candidate sets.

## Profiling Tools Planned Later

Nsight Systems and Nsight Compute remain future tools. Do not run long profiling jobs before CPU/GPU parity tests and a benchmark plan exist.
