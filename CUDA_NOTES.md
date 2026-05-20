# CUDA Notes

## Purpose

This file records CUDA policy for future acceleration work.

## Current CUDA Status

CUDA remains deferred after Stage 4Q. Existing CUDA code is scaffold and smoke-test infrastructure only unless a future stage explicitly adds CPU-reference behavior, unified result-surface review, score-summary parity tests, benchmark-planning acceptance, and benchmark coverage.

Do not use CUDA for Discord processing, image interpretation, OutGuess regression, cookie/hash packs, or broad unsolved-page campaigns.

## RTX 4060 Ti Target

The expected GPU target is RTX 4060 Ti.

## Compute Capability 8.9

RTX 4060 Ti uses compute capability 8.9, represented as CUDA architecture `89` in CMake.

## CMake CUDA Architecture Setting

When CUDA is enabled for smoke/scaffold builds, `CMAKE_CUDA_ARCHITECTURES` defaults to `89` unless the user supplies another value.

## CPU Reference First

Every future CUDA transform must follow a CPU reference implementation. Stage 4H makes `libreprimus.cpu_batch` the current CPU batch parity contract, Stage 4I makes score-summary records the current scoring contract, Stage 4M keeps image/bigram observations out of CUDA scope until reproducible controls exist, Stage 4N keeps stego/audio positive-control readiness out of CUDA scope until fixtures, expected outputs, and toolchains are ready, Stage 4O records deterministic CPU batch parity expectations for expanded adapters, Stage 4P makes result-store and score-summary surfaces comparable, and Stage 4Q records benchmark/parity planning gates. CPU behavior, scoring semantics, reset/advance policy, review state, output records, unified result surfaces, parity expectations, and benchmark scope must be stable before acceleration.

## Future First CUDA Target

The likely first serious CUDA target is batch transform-and-score parity for already-reviewed CPU transforms after observation review hardening, source-lock readiness, image-preflight controls, positive-control readiness, Stage 4O parity expectations, Stage 4P result-store/score-summary unification, and Stage 4Q CPU benchmark/parity planning. Stage 5A is CUDA planning and parity scaffolding only. Hash cracking, Discord processing, image stego fishing, audio/stego extraction, OCR, AI/ML interpretation, and raw data processing are not CUDA targets.

## Parity Tests

Every CUDA kernel must have CPU/GPU parity tests before optimization. Parity tests must include known inputs, negative controls, edge cases, deterministic output comparisons, matching Stage 4H `output_text_hash` / `output_token_hash` records, Stage 4O parity expectation records for supported adapters, Stage 4P unified result surfaces for cross-stage score/status comparison, and Stage 4Q parity readiness gates.

## No Fast-Math Default

Do not enable fast math by default. Cryptanalytic scoring must remain reproducible.

## Memory Layout Planned Later

Memory layouts will be chosen after CPU transform, batch, and scoring APIs are stable.

## Top-K Only Output Principle

GPU kernels should return compact top-k or score summaries instead of dumping huge candidate sets.

## Profiling Tools Planned Later

Nsight Systems and Nsight Compute remain future tools. Do not run long profiling jobs before CPU/GPU parity tests and a benchmark plan exist.
