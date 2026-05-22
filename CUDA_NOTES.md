# CUDA Notes

## Purpose

This file records CUDA policy for future acceleration work.

## Stage 5X Prime-Minus-One Native Parity

Stage 5X is complete. It records no-GPU Python-reference native run records, parity records, result-store preflight records, score-summary preflight records, a full-p56 blocker, guardrails, and next-stage decisions without running CUDA, modifying CUDA source, adding kernels, running native/CUDA CMake, or benchmarking.

Stage 5X executes only the Stage 5W ready synthetic and bounded p56 mappings. The full p56 mapping remains blocked until a complete committed token buffer is scoped. It selects `Stage 5Y - prime-minus-one native parity reporting and CUDA contract readiness gate`.

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

CUDA remains deferred after Stage 5X except for the selected synthetic-only `shift_score_kernel` parity target, its reporting/audit/contract/preparation metadata, the Stage 5J synthetic numeric `gematria_mod29_shift_score_kernel`, the Stage 5M exact solved-fixture-safe parity run, Stage 5N reporting/gate records, Stage 5O exact repeat/result-store preflight records, Stage 5P compact result-store integration records, Stage 5Q metadata-only expansion candidate mapping records, the Stage 5R exact three-candidate expanded solved-fixture parity run, Stage 5S compact reporting/integration records, Stage 5T readiness matrix records, Stage 5U Candidate Batch ABI contract records, Stage 5V no-GPU conformance records, Stage 5W prime-minus-one native contract records, and Stage 5X no-GPU prime-minus-one native parity records. Existing CUDA code is scaffold, smoke-test infrastructure, the Stage 5F synthetic fixture kernel, Stage 5G conservative CUDA-C subset hardening, Stage 5H Gematria mod-29 contract records, Stage 5I Gematria CUDA preparation records, Stage 5J synthetic Gematria parity records, Stage 5K Gematria parity-reporting/preflight records, Stage 5L solved-fixture-safe token-mapping/native-fixture records, Stage 5M host-runner-only solved-fixture parity plumbing, Stage 5O repeat-verification metadata, Stage 5P metadata-only result-store integration, Stage 5Q non-execution candidate mapping, Stage 5R expanded parity metadata, Stage 5S compact integration metadata, Stage 5T solved-family readiness metadata, Stage 5U Candidate Batch ABI metadata, Stage 5V no-GPU conformance metadata, Stage 5W prime-minus-one native contract metadata, and Stage 5X no-GPU prime-minus-one native parity metadata unless a future stage explicitly adds CPU-reference behavior, native CPU parity behavior, unified result-surface review, score-summary parity tests, benchmark-planning acceptance, Stage 5A planning-gate acceptance, Stage 5B harness acceptance, Stage 5C build/device readiness acceptance, Stage 5D deterministic threading acceptance, Stage 5E first-kernel contract acceptance, Stage 5F synthetic parity acceptance, Stage 5G device-code subset acceptance, Stage 5H numeric Gematria contract acceptance, Stage 5I ABI/vector/checklist acceptance, Stage 5J hash-matching acceptance, Stage 5K solved-fixture-safe blocker reporting, Stage 5L token-mapping acceptance, Stage 5M exact parity acceptance, Stage 5N controlled gate acceptance, Stage 5O repeat/preflight acceptance, Stage 5P generated-body policy acceptance, Stage 5Q candidate-mapping acceptance, Stage 5R exact expanded parity acceptance, Stage 5S generated-body/method-status guardrail acceptance, Stage 5T solved-family readiness classification, Stage 5U ABI contract requirements, Stage 5V native conformance requirements, Stage 5W prime-minus-one contract requirements, Stage 5X no-GPU native parity requirements, explicit future-stage approval, and benchmark coverage.

Do not use CUDA for Discord processing, image interpretation, OutGuess regression, cookie/hash packs, or broad unsolved-page campaigns.

## RTX 4060 Ti Target

The expected GPU target is RTX 4060 Ti.

## Compute Capability 8.9

RTX 4060 Ti uses compute capability 8.9, represented as CUDA architecture `89` in CMake.

## CMake CUDA Architecture Setting

When CUDA is enabled for smoke/scaffold builds, `CMAKE_CUDA_ARCHITECTURES` defaults to `89` unless the user supplies another value. Stage 5C records build profile metadata only; the no-GPU CI profile must remain valid and the local 16 GB profile is optional.

## CPU Reference First

Every future CUDA transform must follow a CPU reference implementation. Stage 4H makes `libreprimus.cpu_batch` the current CPU batch parity contract, Stage 4I makes score-summary records the current scoring contract, Stage 4M keeps image/bigram observations out of CUDA scope until reproducible controls exist, Stage 4N keeps stego/audio positive-control readiness out of CUDA scope until fixtures, expected outputs, and toolchains are ready, Stage 4O records deterministic CPU batch parity expectations for expanded adapters, Stage 4P makes result-store and score-summary surfaces comparable, Stage 4Q records benchmark/parity planning gates, Stage 5A records target plans, non-targets, parity scaffolds, and implementation gates, Stage 5B records harness plans, parity fixtures, backend capability profiles, and future-kernel matrix rows, Stage 5C records CUDA build/device metadata, Stage 5D records native C++ CPU threading parity, Stage 5E selects the first future kernel contract, Stage 5F records synthetic parity for that contract, Stage 5G records parity reporting plus conservative device-code subset compliance, Stage 5H records the numeric Gematria mod-29 contract plus native fixture hash, Stage 5I records the Gematria CUDA-C ABI plan and validation vectors, Stage 5J records synthetic Gematria CUDA/native hash parity, Stage 5K reports that parity while keeping solved-fixture-safe CUDA blocked, Stage 5L records source-backed solved-fixture token buffers plus native output-token hashes, Stage 5M records exact solved-fixture CUDA/native hash parity, Stage 5N reports that parity with controlled expansion gates, Stage 5O repeats the exact pack with result-store preflight, Stage 5P integrates compact metadata into result-store and score-summary surfaces, Stage 5Q maps three additional source-backed direct-translation solved-fixture-safe candidates without CUDA execution, Stage 5R runs only those three candidates through the existing kernel and matches their native hashes, Stage 5S integrates only compact reporting metadata while keeping generated bodies unpublished and method statuses unsolved, Stage 5U defines the shared Candidate Batch ABI, Stage 5V proves no-GPU Candidate Batch ABI conformance through Python reference fixtures, Stage 5W prepares prime-minus-one stream native parity contracts, and Stage 5X executes only two no-GPU prime-minus-one native parity mappings while keeping full p56 blocked. CPU behavior, scoring semantics, reset/advance policy, review state, output records, unified result surfaces, parity expectations, benchmark scope, Stage 5A planning gates, Stage 5B harness records, Stage 5C build/device records, Stage 5D native output hashes, Stage 5E contract records, Stage 5F synthetic parity records, Stage 5G reporting/audit records, Stage 5H Gematria contract records, Stage 5I preparation records, Stage 5J kernel records, Stage 5K parity/preflight records, Stage 5L token-mapping/native-hash records, Stage 5M parity/boundary records, Stage 5N gate records, Stage 5O repeat/preflight records, Stage 5P result-store integration records, Stage 5Q expansion candidate records, Stage 5R expanded parity records, Stage 5S compact integration records, Stage 5U ABI contracts, Stage 5V native conformance records, Stage 5W prime-minus-one native contract records, and Stage 5X no-GPU native parity records must be stable before acceleration.

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
