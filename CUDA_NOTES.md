# CUDA Notes

## Purpose

This file records CUDA policy for future acceleration work.

## Stage 5AD Bounded P56 CUDA Parity

Stage 5AD is complete. It ran only `stage5z-validation-p56-bounded-v0` through the existing `prime_minus_one_stream_kernel_v0` path and recorded CUDA attempted/pass/fail/skip `1/0/1/0`.

The Stage 5X expected output-token hash is `4a3059f12c0f8450bd4ef7e31bf879fbc104202e5fb0e53b7ba514241f07cd87`; the computed CUDA hash is `6034fe2431159615449db79c36869236d306768414038314d47d6d57d9ae7387`. Stage 5AD records `failed_hash_mismatch` and selects Stage 5AD-fix mismatch investigation.

Stage 5AD modifies no CUDA-facing `.cu` or `.cuh` source, adds no kernels, runs no full p56 or unsolved-page CUDA, runs no benchmarks, executes no scored experiments, processes no raw data, expands no website, and makes no solve claim.

## Stage 5AC Prime-Minus-One CUDA Synthetic Reporting

Stage 5AC is complete. It reports Stage 5AA synthetic prime-minus-one CUDA parity into compact result-store and score-summary metadata, preserves method-status and generated-body guardrails, validates the Stage 5AB doc-staleness gate, and preflights only the bounded p56 vector for a future explicit Stage 5AD run.

## Stage 5AB Document Staleness Gate

Stage 5AB is complete. It adds dynamic current/next-stage document staleness checks, a committed source-of-truth record, an operational file map, and CI integration. It repairs stale operational Markdown after Stage 5AA and enables Stage 5AC to consume the Stage 5AA outcome after stale-doc repair.

## Stage 5AA Prime-Minus-One CUDA Synthetic Parity

Stage 5AA is complete. It adds `prime_minus_one_stream_kernel_v0` for the single synthetic Stage 5Z validation vector and records CUDA attempted/pass/fail/skip `1/1/0/0` with the expected and computed hash `06a5c37f7e5eda8eec00cfab5b09faba6ec157488ca15f61a9189d4bf06005ab`.

This is synthetic correctness metadata only. It does not authorize p56/full-p56 CUDA, unsolved-page CUDA, scored experiments, benchmarking, generated-body publication, website expansion, method-status upgrades, canonical corpus activation, page-boundary finalisation, or solve claims. Stage 5AC consumes this output as compact reporting/preflight metadata.

## Stage 5Z Prime-Minus-One CUDA Contract

Stage 5Z is complete. It records prime-minus-one CUDA contract metadata, CUDA-C style kernel ABI records, host-runner contract records, buffer contracts, validation vectors, future parity plans, result-store compatibility, full-p56 blocker preservation, scored-experiment deferral, implementation-readiness gates, and next-stage decisions without native execution, CUDA execution, CUDA source changes, kernels, native/CUDA CMake, or benchmarking.

Stage 5Z selects `Stage 5AA - prime-minus-one CUDA synthetic kernel implementation and parity`. The Stage 5AA scope must remain synthetic-only unless that prompt explicitly widens it. Full p56, p56 fixture CUDA, unsolved pages, scored experiments, benchmarks, generated-body publication, method-status upgrades, and solve claims remain blocked.

## Stage 5Y Prime-Minus-One Native Reporting

Stage 5Y is complete. It records compact prime-minus-one native parity reports, Stage 4P-compatible result-store integration, Stage 4I-compatible score-summary integration, method-status impact, generated-body policy, full-p56 blocker preservation, CUDA contract readiness, bounded scored-experiment readiness, guardrails, and next-stage decision records without rerunning native parity, running CUDA, modifying CUDA source, adding kernels, running native/CUDA CMake, or benchmarking.

Stage 5Y marks only `Stage 5Z - prime-minus-one CUDA contract preparation` ready. CUDA execution, source changes, kernel implementation, full p56 execution, unsolved-page CUDA, GPU benchmarks, and speedup claims remain blocked.

## Stage 5X Prime-Minus-One Native Parity

Stage 5X is complete. It records no-GPU Python-reference native run records, parity records, result-store preflight records, score-summary preflight records, a full-p56 blocker, guardrails, and next-stage decisions without running CUDA, modifying CUDA source, adding kernels, running native/CUDA CMake, or benchmarking.

Stage 5X executes only the Stage 5W ready synthetic and bounded p56 mappings. The full p56 mapping remains blocked until a complete committed token buffer is scoped. Stage 5Y consumes those records for compact reporting.

## Stage 5W Prime-Minus-One Native Contract

Stage 5W is complete. It records source inventory, source-backed prime-minus-one stream contract, deterministic prime schedule, Candidate Batch ABI v0 mapping, native parity preparation, result-store preflight, guardrails, and next-stage decision records without running CUDA, modifying CUDA source, adding kernels, running native/CUDA CMake, or benchmarking.

The Stage 5W contract kept the bounded Stage 4O/5L p56 mapping ready for Stage 5X no-GPU native parity execution and keeps full p56 parity blocked until a complete committed token buffer is scoped.

## Stage 5V Native Candidate Batch ABI Conformance

Stage 5V is complete. It records native Candidate Batch ABI adapter metadata, seven raw-data-free conformance fixtures, three Python reference output-token hashes, token-buffer conformance, key/stream schedule shape conformance, score-vector/top-k conformance, compact result-store conformance, implementation-status records, and next-stage decision records without running CUDA, modifying CUDA source, adding kernels, running native/CUDA CMake, or benchmarking.

The Stage 5V adapter surface is a no-GPU Python reference path only. It proves shared ABI shape and hashing rules before family-specific native contracts; it leaves C++ adapter implementation deferred and selects `Stage 5W - prime-minus-one stream native parity contract preparation`.

## Stage 5U Candidate Batch ABI

Stage 5U is complete. It defines Candidate Batch ABI v0 plus token-buffer, transform-parameter, key-schedule, stream-schedule, score-vector, top-k, backend-surface, result-store compatibility, Stage 5T ABI gap closure, and next-stage decision records without running CUDA, modifying CUDA source, adding kernels, or benchmarking.

The Stage 5U ABI is a contract boundary for future no-GPU native reference conformance. It keeps Gematria token values `0..28`, separator placeholders, transformable masks, candidate-major ordering, Stage 4I triage-only score semantics, and Stage 4P compact result-store policy explicit. It does not authorize original transform-family CUDA semantics or performance claims.

Stage 5U selected `Stage 5V - native candidate batch ABI reference adapter and conformance fixtures`.

## Stage 5T Solved-Family Readiness

Stage 5T is complete. It records a solved-family CUDA readiness matrix and kernel-readiness classification without running CUDA, modifying CUDA source, adding kernels, or benchmarking.

The Stage 5T matrix distinguishes existing `gematria_shift_score_only` parity from original transform-family semantics. Direct-translation fixture buffers have supported solved-fixture parity for the existing kernel, but direct translation, reverse Gematria, rotated reverse Gematria, explicit-key Vigenere, and prime-minus-one original semantics are not CUDA-verified.

Stage 5T selected `Stage 5U - unified candidate batch ABI and backend contract consolidation` because future kernels need shared token buffer, key schedule, stream schedule, score-vector, and top-k output surfaces before more CUDA contracts are responsible.

## Current CUDA Status

CUDA remains deferred after Stage 5AD except for explicitly scoped synthetic or solved-fixture-safe parity stages. Existing CUDA code and metadata are summarized by the latest staged-plan and CUDA notes; broad CUDA and unsolved-page CUDA remain blocked unless an explicit future prompt scopes them with CPU references, parity tests, result records, and benchmark plans. Stage 5Z prime-minus-one CUDA contract records, Stage 5AA synthetic CUDA records, Stage 5AC reporting/preflight records, and Stage 5AD bounded mismatch records are not full p56 parity, benchmark evidence, or solve evidence.

Do not use CUDA for Discord processing, image interpretation, OutGuess regression, cookie/hash packs, or broad unsolved-page campaigns.

## RTX 4060 Ti Target

The expected GPU target is RTX 4060 Ti.

## Compute Capability 8.9

RTX 4060 Ti uses compute capability 8.9, represented as CUDA architecture `89` in CMake.

## CMake CUDA Architecture Setting

When CUDA is enabled for smoke/scaffold builds, `CMAKE_CUDA_ARCHITECTURES` defaults to `89` unless the user supplies another value. Stage 5C records build profile metadata only; the no-GPU CI profile must remain valid and the local 16 GB profile is optional.

## CPU Reference First

Every future CUDA transform must follow a CPU reference implementation. Stage 4H makes `libreprimus.cpu_batch` the current CPU batch parity contract, Stage 4I makes score-summary records the current scoring contract, Stage 4M keeps image/bigram observations out of CUDA scope until reproducible controls exist, Stage 4N keeps stego/audio positive-control readiness out of CUDA scope until fixtures, expected outputs, and toolchains are ready, Stage 4O records deterministic CPU batch parity expectations for expanded adapters, Stage 4P makes result-store and score-summary surfaces comparable, Stage 4Q records benchmark/parity planning gates, Stage 5A records target plans, non-targets, parity scaffolds, and implementation gates, Stage 5B records harness plans, parity fixtures, backend capability profiles, and future-kernel matrix rows, Stage 5C records CUDA build/device metadata, Stage 5D records native C++ CPU threading parity, Stage 5E selects the first future kernel contract, Stage 5F records synthetic parity for that contract, Stage 5G records parity reporting plus conservative device-code subset compliance, Stage 5H records the numeric Gematria mod-29 contract plus native fixture hash, Stage 5I records the Gematria CUDA-C ABI plan and validation vectors, Stage 5J records synthetic Gematria CUDA/native hash parity, Stage 5K reports that parity while keeping solved-fixture-safe CUDA blocked, Stage 5L records source-backed solved-fixture token buffers plus native output-token hashes, Stage 5M records exact solved-fixture CUDA/native hash parity, Stage 5N reports that parity with controlled expansion gates, Stage 5O repeats the exact pack with result-store preflight, Stage 5P integrates compact metadata into result-store and score-summary surfaces, Stage 5Q maps three additional source-backed direct-translation solved-fixture-safe candidates without CUDA execution, Stage 5R runs only those three candidates through the existing kernel and matches their native hashes, Stage 5S integrates only compact reporting metadata while keeping generated bodies unpublished and method statuses unsolved, Stage 5U defines the shared Candidate Batch ABI, Stage 5V proves no-GPU Candidate Batch ABI conformance through Python reference fixtures, Stage 5W prepares prime-minus-one stream native parity contracts, Stage 5X executes only two no-GPU prime-minus-one native parity mappings while keeping full p56 blocked, and Stage 5Y integrates compact reporting/readiness metadata before Stage 5Z contract preparation. CPU behavior, scoring semantics, reset/advance policy, review state, output records, unified result surfaces, parity expectations, benchmark scope, Stage 5A planning gates, Stage 5B harness records, Stage 5C build/device records, Stage 5D native output hashes, Stage 5E contract records, Stage 5F synthetic parity records, Stage 5G reporting/audit records, Stage 5H Gematria contract records, Stage 5I preparation records, Stage 5J kernel records, Stage 5K parity/preflight records, Stage 5L token-mapping/native-hash records, Stage 5M parity/boundary records, Stage 5N gate records, Stage 5O repeat/preflight records, Stage 5P result-store integration records, Stage 5Q expansion candidate records, Stage 5R expanded parity records, Stage 5S compact integration records, Stage 5U ABI contracts, Stage 5V native conformance records, Stage 5W prime-minus-one native contract records, Stage 5X no-GPU native parity records, and Stage 5Y reporting/readiness records must be stable before acceleration.

## Future First CUDA Target

The selected first CUDA contract is `shift_score_kernel` for `caesar_mod29`, backed by the Stage 5E `native_cpu_synthetic_shift_adapter` mapping and Stage 5D native output hash. Stage 5F implements only that synthetic-only parity kernel over uppercase Latin A-Z fixture text and shifts, Stage 5G reports the hash match while keeping solved-fixture CUDA blocked, Stage 5H defines future production Gematria mod-29 behavior separately, Stage 5I prepares the future `gematria_mod29_shift_score_kernel` ABI, Stage 5J implements only the synthetic numeric parity kernel for raw tokens `0..28`, `(token + shift) % 29`, transformable masks, deterministic candidate ordering, and preserved separator tokens, Stage 5K records parity/preflight blockers without CUDA execution, Stage 5L prepares solved-fixture-safe token buffers and CPU/native output-token hashes without CUDA execution, and Stage 5M runs the existing kernel over those exact buffers. Hash cracking, Discord processing, image stego fishing, audio/stego extraction, OCR, AI/ML interpretation, website expansion, and raw data processing are not CUDA targets.

## Parity Tests

Every CUDA kernel must have CPU/GPU parity tests before optimization. Parity tests must include known inputs, negative controls, edge cases, deterministic output comparisons, matching Stage 4H `output_text_hash` / `output_token_hash` records, Stage 4O parity expectation records for supported adapters, Stage 4P unified result surfaces for cross-stage score/status comparison, Stage 4Q parity readiness gates, Stage 5A target/scaffold/gate records, Stage 5B harness/fixture/backend/matrix records, Stage 5C build/device records, Stage 5D native CPU threading/parity records, Stage 5E first-kernel contract records, Stage 5F synthetic parity records, Stage 5G parity-reporting/device-code audit records, Stage 5H Gematria contract/native fixture records, Stage 5I ABI/vector records, Stage 5J Gematria CUDA kernel parity records, Stage 5K Gematria parity-reporting/preflight records, Stage 5L solved-fixture token-mapping/native parity records, Stage 5M solved-fixture CUDA parity/boundary records, Stage 5N controlled expansion gate records, Stage 5O repeat parity/result-store preflight records, Stage 5U Candidate Batch ABI contracts, and Stage 5V native conformance fixtures.

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
