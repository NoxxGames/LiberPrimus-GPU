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

## Stage 5T Benchmark-Readiness Boundary

Stage 5T records benchmark-readiness planning metadata only. It writes three benchmark-readiness records: CPU baseline planning, CUDA microbenchmark planning blocked pending Stage 5U ABI work, and end-to-end speedup claims blocked as non-evidence.

Stage 5T does not run CUDA, native/CUDA CMake, profilers, timing loops, or benchmark commands. Do not report Stage 5T validation output, readiness counts, or generated reports as performance evidence.

## Stage 5U Candidate Batch ABI Boundary

Stage 5U is not a benchmark stage. It defines Candidate Batch ABI v0 and backend contracts only. It closes Stage 5T ABI gaps by contract and selects Stage 5V native no-GPU conformance fixtures before any benchmark refresh.

Do not report Stage 5U validation output, contract counts, ABI gap closure counts, or generated reports as throughput, performance, or speedup evidence.

## Stage 5V Native Candidate Batch ABI Conformance Boundary

Stage 5V is not a benchmark stage. It runs only raw-data-free Python reference fixture conformance, records deterministic output-token hashes, and validates score-vector/top-k/result-store shape metadata. It does not run CUDA, native/CUDA CMake, GPU benchmarks, timing loops, profilers, or speedup measurements.

Do not report Stage 5V conformance counts, output hashes, implementation-status rows, or generated reports as throughput, performance, or speedup evidence. Stage 5W may prepare a family-specific native parity contract, but GPU benchmarking remains blocked.

## Stage 5W Prime-Minus-One Native Contract Boundary

Stage 5W is not a benchmark stage. It records source-backed prime-minus-one stream contracts, deterministic schedule records, p56 readiness metadata, and result-store preflight records without running native parity, CUDA, native/CUDA CMake, profilers, timing loops, or benchmark commands.

Do not report Stage 5W record counts, p56 readiness, schedule metadata, or generated reports as throughput, performance, or speedup evidence. Stage 5X may execute no-GPU native parity only if scoped by Stage 5W records; GPU benchmarking remains blocked.

## Stage 5X Prime-Minus-One Native Parity Boundary

Stage 5X is not a benchmark stage. It records no-GPU Python-reference native parity for two ready Stage 5W mappings, keeps full p56 blocked, and writes result-store and score-summary preflight metadata without CUDA, native/CUDA CMake, profilers, timing loops, or benchmark commands.

Do not report Stage 5X pass counts, output hashes, blocker status, or generated reports as throughput, performance, or speedup evidence. Stage 5Y may report compact readiness metadata only; GPU benchmarking remains blocked.

## Stage 5Y Prime-Minus-One Native Reporting Boundary

Stage 5Y is not a benchmark stage. It records compact parity reports, result-store and score-summary integration rows, generated-body policy rows, full-p56 blocker preservation, readiness gates, guardrails, and next-stage decisions without native execution, CUDA execution, native/CUDA CMake, profilers, timing loops, or benchmark commands.

Do not report Stage 5Y record counts, readiness gates, output hashes, blocker status, or generated reports as throughput, performance, or speedup evidence. Stage 5Z may prepare contracts only; GPU benchmarking remains blocked.

## Stage 5AA Prime-Minus-One CUDA Synthetic Boundary

Stage 5AA executes only the synthetic prime-minus-one validation vector. The local CUDA pass and matching hash are correctness metadata, not timing, throughput, performance, or speedup evidence. Do not cite Stage 5AA as a benchmark. GPU benchmarking, p56/full-p56 CUDA, scored experiments, and unsolved-page CUDA remain blocked.

## Stage 5AC Prime-Minus-One CUDA Synthetic Reporting Boundary

Stage 5AC reports Stage 5AA synthetic parity metadata and preflights a future bounded-p56 CUDA parity run. It performs no CUDA execution, no p56 execution, no native execution, no GPU benchmark, no speedup measurement, and no performance claim.

## Stage 5AD Bounded P56 CUDA Parity Boundary

Stage 5AD runs only one bounded p56 CUDA parity vector and records a hash mismatch. The run is correctness metadata, not timing, throughput, performance, or speedup evidence. Do not cite Stage 5AD CUDA attempted/pass/fail counts, CMake/CTest status, or output hashes as benchmark results. Full p56, unsolved pages, profilers, timing loops, and speedup claims remain blocked.

## Stage 5AD-fix Mismatch Investigation Boundary

Stage 5AD-fix is a no-GPU diagnostic/reporting stage. It traces hash lineage, token/stream/formula material, and reference-contract status only. Do not cite Stage 5AD-fix as a benchmark, speedup, throughput, CUDA parity pass, full p56 result, or solve result.

## Stage 5AE Corrected Formula Reporting Boundary

Stage 5AE is not a benchmark stage. It records corrected bounded p56 formula-parity metadata and reference-contract/hash-material policy repairs only. Do not cite Stage 5AE record counts, corrected formula hash equality, or generated reports as throughput, performance, speedup, full p56 parity, or solve evidence.

## Stage 5AH Doc-Staleness Boundary

Stage 5AH is not a benchmark stage. It records operational documentation staleness, stage-ledger coverage, current/next-stage consistency, and operational-file-map coverage only. Do not cite Stage 5AH record counts, clean staleness reports, or generated reports as throughput, performance, speedup, CUDA parity, source extraction evidence, or solve evidence.

## Stage 5Z Prime-Minus-One CUDA Contract Boundary

Stage 5Z is not a benchmark stage. It records prime-minus-one CUDA contract, kernel ABI, host-runner, buffer, validation-vector, future parity, result-store compatibility, full-p56 blocker, scored-experiment deferral, implementation-readiness, and next-stage decision metadata without native execution, CUDA execution, native/CUDA CMake, profilers, timing loops, or benchmark commands.

Do not report Stage 5Z record counts, validation-vector readiness, implementation-readiness gates, or generated reports as throughput, performance, or speedup evidence. Stage 5AA may implement only a synthetic-only kernel parity path if scoped by its prompt; GPU benchmarking remains blocked.

## Stage 4Q CPU Benchmark Planning

Stage 4Q records benchmark planning and parity readiness only. It writes committed CPU benchmark plan and CUDA parity readiness metadata, plus ignored environment and CPU smoke diagnostics under `experiments/results/benchmarks/stage4q/`.

Stage 4Q CPU smoke timings are diagnostic only. They are not performance claims, speedup evidence, CUDA benchmarks, or authorization to implement GPU kernels.

Stage 5A uses Stage 4Q records for CUDA planning and parity scaffolding only. It records target plans, non-targets, parity scaffolds, and implementation gates without running GPU benchmarks or making speedup claims. Stage 5B records a CUDA parity harness skeleton, backend capability profiles, and future-kernel matrix rows without running GPU benchmarks or making speedup claims. Stage 5C records CUDA build profiles, toolchain detection, device detection, and optional smoke-build status without running GPU benchmarks or making speedup claims. Stage 5D records native C++ CPU backend diagnostics and threading parity without GPU benchmarks or speedup claims. Stage 5E records first-kernel contract selection without GPU benchmarks or speedup claims. Stage 5F records a synthetic parity kernel and optional local build/parity status without GPU benchmarks or making speedup claims. Stage 5G records parity reporting, CUDA-C subset hardening, and solved-fixture-safe blockers without running GPU benchmarks or making speedup claims. Stage 5H records Gematria mod-29 contract and native fixture metadata without running GPU benchmarks or making speedup claims. Stage 5I records Gematria CUDA preparation metadata without running GPU benchmarks or making speedup claims. Stage 5J records synthetic Gematria CUDA build/parity correctness metadata without running GPU benchmarks or making speedup claims. Stage 5K records Gematria parity reporting, device-code audit status, solved-fixture-safe blockers, and score-summary preflight metadata without running CUDA, GPU benchmarks, or making speedup claims. Stage 5L records solved-fixture-safe token mappings and native output-token hashes without running CUDA, GPU benchmarks, or making speedup claims. Stage 5M records exact solved-fixture-safe CUDA/native parity without GPU benchmarks or speedup claims. Stage 5N reports that parity and records controlled expansion gates without running CUDA, GPU benchmarks, or making speedup claims. Stage 5O repeats the exact Stage 5M pack for correctness and result-store preflight without GPU benchmarks or speedup claims. Stage 5P integrates compact result-store and score-summary metadata without running CUDA, GPU benchmarks, or making speedup claims. Stage 5Q maps additional solved-fixture-safe candidates and native hashes without running CUDA, GPU benchmarks, or making speedup claims. Stage 5R runs exactly those three mapped candidates for correctness parity and records no GPU benchmark, speedup, or performance claim. Stage 5S integrates Stage 5R compact metadata into result-store/score-summary records and also records no GPU benchmark, speedup, or performance claim. Stage 5T classifies solved-family readiness and benchmark-planning blockers without running CUDA, native/CUDA CMake, GPU benchmarks, or making speedup claims. Stage 5U defines Candidate Batch ABI contracts without running CUDA, native/CUDA CMake, GPU benchmarks, or making speedup claims. Stage 5V validates no-GPU ABI conformance with raw-data-free Python fixtures and still records no benchmark, speedup, or performance claim. Stage 5W prepares prime-minus-one native contracts without native/CUDA execution or benchmark evidence. Stage 5X executes no-GPU Python-reference parity for two ready mappings and records no benchmark, speedup, or performance claim. Stage 5Y reports compact readiness metadata without execution or benchmark evidence. Stage 5AB is a document staleness quality gate. Stage 5AC reports Stage 5AA compact metadata and bounded-p56 preflight records without CUDA execution, native execution, or benchmarks. Stage 5AD runs one bounded CUDA parity vector but still records no benchmark or speedup evidence. Stage 5AD-fix traces the mismatch without CUDA execution or benchmark evidence. Stage 5AF and Stage 5AG are local source-harvester/source-inventory metadata stages, and Stage 5AH is a doc-staleness quality gate; none are benchmark stages. Website expansion is deferred to a future unnumbered project.

## Stage 5P Result-Store Integration Boundary

Stage 5P result-store integration is reporting metadata only. It records compact hashes and policy
rows from Stage 5O and does not run benchmark commands, profile kernels, claim throughput, or publish
generated CUDA result bodies.

## Stage 5Q Expansion Candidate Mapping Boundary

Stage 5Q expansion candidate mapping is metadata only. It records three additional source-backed
direct-translation solved-fixture-safe token mappings and native output-token hashes for future
parity, not performance measurements or CUDA throughput. Do not cite Stage 5Q records as a
benchmark or speedup result.

## Stage 5R Expanded CUDA Parity Boundary

Stage 5R expanded solved-fixture CUDA parity is correctness metadata only. It runs exactly the
three Stage 5Q mapped direct-translation candidates through the existing Gematria kernel and
matches their native hashes. Do not cite Stage 5R as a GPU benchmark, throughput measurement,
or speedup claim.

## Stage 5S Reporting Boundary

Stage 5S is not a benchmark stage. It does not run CUDA or native/CUDA CMake. It consumes compact Stage 5R metadata, writes result-store and score-summary integration records, and explicitly records `gpu_benchmark_performed=false`, `speedup_claim=false`, and `performance_claim=false`.

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

## Stage 5F Synthetic Kernel Boundary

Stage 5F implements and optionally runs only the synthetic `shift_score_kernel` parity test. The
recorded local CUDA build/parity status is correctness metadata, not benchmark metadata. Do not
report Stage 5F timing, build, or CTest output as performance, throughput, or speedup evidence.

## Stage 5G Parity Reporting Boundary

Stage 5G reports the Stage 5F hash match and audits CUDA-facing source style. The reports are
readiness metadata only. Do not report Stage 5G build, audit, CTest, or validation output as
throughput evidence.

## Stage 5H Gematria Contract Boundary

Stage 5H defines numeric Gematria mod-29 shift semantics and a synthetic native fixture hash. The
records are contract metadata only. Do not report Stage 5H validation, fixture hashes, or CTest
output as throughput evidence.

## Stage 5I Gematria CUDA Preparation Boundary

Stage 5I defines the future Gematria CUDA-C ABI, validation vectors, and Stage 5J checklist only.
The records are preparation metadata, not kernel execution or benchmark metadata. Do not report
Stage 5I validation, vector hashes, generated reports, or native fixture hashes as throughput
evidence.

## Stage 5J Gematria CUDA Kernel Boundary

Stage 5J implements and optionally runs only the synthetic numeric
`gematria_mod29_shift_score_kernel` parity test. The local CUDA build and parity status is
correctness metadata, not benchmark metadata. Do not report Stage 5J build, CTest, validation,
kernel output hash, or generated reports as throughput, performance, or speedup evidence.

## Stage 5K Gematria CUDA Parity Reporting Boundary

Stage 5K reports the Stage 5J Gematria CUDA/native hash match and records solved-fixture-safe
preflight blockers. It does not run CUDA, modify CUDA source, add kernels, execute solved or
unsolved page data, run GPU benchmarks, or make speedup claims. Do not report Stage 5K validation,
device-code audit, blockers, or generated reports as throughput, performance, or speedup evidence.

## Stage 5L Solved-Fixture Token Mapping Boundary

Stage 5L maps committed solved-fixture-safe streams into Gematria `0..28` token buffers and records
CPU/native output-token hashes. It does not run CUDA, modify CUDA source, add kernels, execute
solved or unsolved page data through CUDA, run GPU benchmarks, or make speedup claims. Do not report
Stage 5L validation, native hashes, blocker reduction, or generated reports as throughput,
performance, or speedup evidence.

## Stage 5M Solved-Fixture CUDA Parity Boundary

Stage 5M runs only the existing `gematria_mod29_shift_score_kernel` over exactly five Stage 5L
mapped solved-fixture-safe token buffers. The local CUDA/native hash matches are correctness
metadata only. Do not report Stage 5M CMake, CTest, run status, kernel output hashes, or generated
reports as throughput, performance, or speedup evidence.

## Stage 5N Reporting Gate Boundary

Stage 5N does not run CUDA. It reports Stage 5M parity and records controlled expansion gates.
Do not report Stage 5N gate status, parity report counts, or result-store preflight metadata as
throughput, performance, or speedup evidence.

## Stage 5O Repeat Verification Boundary

Stage 5O may run only the exact Stage 5M solved-fixture-safe CUDA buffer set. It records repeat
hash correctness and result-store preflight metadata, not benchmark, throughput, performance, or
speedup evidence.

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
