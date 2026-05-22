> This Wiki page mirrors $sourceRel. The repository tutorial file is the source of truth.

# Hardware And Performance

## CPU/GPU Responsibility Split

CPU code owns corpus management, manifests, orchestration, provenance, branching search, and review.

GPU code will later accelerate large regular transform-and-score batches only after CPU references and parity tests exist.

Stage 2E dry-run manifests may estimate future CPU candidate counts, but they do not run benchmarks, execute search, or use CUDA. Treat those counts as planning metadata only.

## Current Stage

Stage 5E records first CUDA kernel contract and CPU/native parity adapter metadata only. Stage 5F implements only the selected synthetic `shift_score_kernel` parity target. Stage 5G reports that parity, audits CUDA-facing source style, and keeps solved-fixture CUDA blocked. Stage 5J implements only the synthetic numeric `gematria_mod29_shift_score_kernel` parity target. Stage 5K reports that hash match, audits the device-code subset, and keeps solved-fixture CUDA blocked. Stage 5L maps solved-fixture-safe token buffers and native hashes without CUDA execution. Stage 5M runs only the existing Gematria kernel over the exact five Stage 5L buffers and records hash parity. Stage 5O repeats that exact pack. Stage 5P integrates compact result-store and score-summary metadata without running CUDA. Stage 5Q maps three additional solved-fixture-safe direct-translation candidates and native hashes without running CUDA. Stage 5R runs those three mapped candidates for correctness parity only. Stage 5S reports and integrates those compact hashes without running CUDA. Stage 5T classifies solved-family readiness. Stage 5U defines shared Candidate Batch ABI contracts. Stage 5V proves no-GPU ABI conformance through Python reference fixtures. Stage 5W prepares prime-minus-one native contract records. Stage 5X executes only the two ready no-GPU prime-minus-one native parity mappings and keeps full p56 blocked. Stage 5Y integrates compact prime-minus-one native reporting and CUDA contract readiness-gate metadata. Stage 5Z prepares the prime-minus-one CUDA contract, kernel ABI, host-runner, buffer, validation-vector, and readiness records without native execution or CUDA execution. Stage 5AA runs only the synthetic prime-minus-one CUDA validation vector. Stage 5AB is a document-staleness quality gate and does not run CUDA, native execution, or benchmarks. None of these stages run GPU benchmarks or make speedup claims.

## Design Assumptions

The project notes an RTX 4060 Ti and i9-9900K as a development target, but users do not need identical hardware for current tools.

## Future GPU Workloads

Future CUDA kernels may help with batched transforms, scoring, and top-k candidate filtering after correctness is pinned.

## Speed Claims

Do not make public speed claims without committed benchmark methodology, hardware metadata, and reproducible inputs.

## Stage 0D-followup Timing

The follow-up alignment records elapsed milliseconds for parsing, view generation, matching, gap analysis, and boundary audit. Treat these as troubleshooting metadata, not benchmark results. CUDA remains unused because this stage is about transcript structure and provenance, not batch transform/scoring.

## Stage 0E Timing

Corpus candidate generation records lightweight timing for profile validation and tokenization. It is CPU-only and does not imply future CUDA performance.

## Stage 1A Timing

Direct fixture reproduction is CPU-only and fast. It is a correctness check before future cipher work, not a performance workload.
## Stage 1B Performance Note

Stage 1B Atbash-family reproduction is CPU-only and small. It does not use CUDA, and it should not be treated as a GPU benchmark.

GPU acceleration remains future-facing for larger transform and scoring workloads after CPU references and parity tests exist.

## Stage 5C CUDA Build And Device Detection

Stage 5C records no-GPU CI, compatibility 8 GB, and optional local 16 GB profiles. Toolchain and device records are environment metadata only.

The optional smoke-build path records configure/build status for existing scaffold targets. It does not run CUDA tests, benchmarks, or cryptanalytic kernels, and a local device record is not parity evidence.

## Stage 5D Native CPU Threading

Stage 5D records native CPU backend and threading parity metadata. Matching output hashes across
thread counts are correctness diagnostics for the synthetic fixture, not CPU benchmarks, GPU
benchmarks, or speedup claims. C++ remains a deterministic CPU execution plane and Python remains
orchestration.
## Stage 1C Performance Scope

Stage 1C explicit-key Vigenere reproduction is CPU-only and small. Timing fields in generated summaries are diagnostics, not benchmarks. CUDA is not used.

## Stage 1D Performance Scope

Stage 1D p56 prime-minus-one reproduction is CPU-only and small. Deterministic prime generation is used for fixture correctness, not throughput benchmarking. CUDA and scoring remain out of scope.

## Stage 2A Performance Scope

Stage 2A registry dispatch and solved-baseline manifests are CPU-only regression checks. The elapsed time in `experiments/results/solved-baselines/stage2a/summary.json` is diagnostic metadata only.

Stage 2A does not run search, scoring, CUDA kernels, or throughput benchmarks.

## Stage 2B Result Store Scope

Stage 2B writes generated JSONL and SQLite result stores for the solved-baseline regression import. This is CPU-only bookkeeping and validation, not a benchmark or search workload.

Run the smoke command when you need to verify the local result-store path:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli result-store stage2b-smoke --solved-baseline-manifest experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml --result-store-manifest experiments/manifests/result-store/stage2b-solved-baseline-import.yaml --solved-baseline-out-dir experiments/results/solved-baselines/stage2a --result-store-out-dir experiments/results/result-store/stage2b --replace --allow-warnings
```

Generated JSONL and SQLite files remain ignored. CUDA remains unused.

## Stage 2F Execution Scope

Stage 2F CPU execution is still small correctness plumbing, not a benchmark. It runs synthetic and solved-fixture-only manifests through CPU reference transforms and records ignored outputs. CUDA, scoring, search, and throughput claims remain out of scope.

## Stage 2G Proposal Scope

Stage 2G adds proposal and approval records only. Hardware performance claims remain out of scope because proposals are blocked pending explicit human approval and do not execute.

## Stage 2H Control Execution Scope

Stage 2H approval-gated execution is still not a benchmark stage. Approved controls may run synthetic and solved-fixture-only requests, but real unsolved-page execution, search, scoring, and CUDA remain disabled.

## Stage 3A Minimal CPU Run

Stage 3A is a small local CPU candidate enumeration, not a benchmark campaign. It runs `841` Caesar plus affine candidates for one reviewable slice and writes ignored outputs. Minimal triage scoring is used for sorting leads only. CUDA remains disabled, no throughput claim is made, and no solve claim is made.

## Stage 3B Inspection And Reverse-Direction Run

Stage 3B inspects ignored Stage 3A outputs, reranks candidates with refined local scoring, and runs one reverse-direction `841` candidate CPU comparison. This is still not a benchmark, broad campaign, or CUDA workload. Scores remain triage metadata only, and generated candidate dumps stay ignored.

## Stage 3C Calibration Scope

Stage 3C calibration is CPU-only local scoring work. It scores small positive, null, negative, and candidate control sets, writes ignored outputs, and makes no throughput, CUDA, or solve claim.

## Stage 3D Vigenere Scope

Stage 3D is also CPU-only. It runs exactly four explicit Vigenere keys from a committed queue item, writes ignored generated outputs, and does not justify GPU work or a solve claim.

## Stage 3E Backlog Dry-Run Scope

Stage 3E is CPU planning and dry-run validation only. After Stage 3G queue updates, it validates seven bounded queue items with total candidate estimate `972`, classifies missing executors, writes an ignored dry-run summary, and does not execute queued candidate generation by itself. It is not a benchmark, does not widen into broad key search, and does not justify CUDA work.

## Stage 3F CPU Key-Pack Scope

Stage 3F is still a local CPU-only run. It executes `48` explicit Vigenere candidates from the manifest-bound LP evidence key pack and writes generated outputs to ignored local paths. It is not a performance benchmark, not a dictionary search, and not a reason to start CUDA work.

## Stage 3G Prime Sweep Scope

Stage 3G is still a local CPU-only run. It executes `256` manifest-bound p56-local prime-minus-one offset candidates and writes generated outputs to ignored local paths. It is not a performance benchmark, not a broad number-sequence search, and not a reason to start CUDA work.

## Stage 3H Reset/Advance Scope

Stage 3H is still a local CPU-only run. It executes `64` reset/advance ablation candidates and writes `100` family-specific negative controls to ignored local paths. It is not a benchmark, not a broad search, and not a reason to start CUDA work.

## Stage 3I Historical Vigenere Scope

Stage 3I is still a local CPU-only run. It executes `56` explicit historical motif Vigenere candidates and writes generated outputs to ignored local paths. It is not a dictionary attack, not a broad key search, not a benchmark, and not a reason to start CUDA work.

## Stage 3J Mersenne Probe Scope

Stage 3J is still a local CPU-only run. It executes `192` bounded Mersenne/perfect-number stream candidates from a finite declared exponent sequence and writes generated outputs to ignored local paths. It is not a broad number-theory search, not a benchmark, not a CUDA workload, and not a reason to start GPU work.

## Stage 3K Registry Scope

Stage 3K is registry work only. Deterministic image metadata extraction is lightweight CPU/stdlib work and does not use GPU acceleration, OCR, AI image interpretation, or broad archive crawling.

## Stage 3L Hash Scope

Stage 3L is CPU-only SHA-256 exact matching over small committed candidate packs. It does not use CUDA, GPU hash cracking, hashcat, cloud services, or external dictionaries.

## Stage 3M Image Analysis Scope

Stage 3M is deterministic local CPU image-feature extraction. It uses no CUDA, GPU acceleration, OCR, AI/ML image interpretation, OutGuess, audio tooling, live web acquisition, or benchmark claims. Generated image-analysis records remain ignored.

## Stage 3N Discord Ingestion Scope

Stage 3N is local HTML parsing and source-discovery indexing only. It uses no CUDA, GPU acceleration, browser automation, live Discord APIs, scraping, self-bots, AI upload, or benchmark claims. Generated Discord ingestion records and local review indexes remain ignored.

## Stage 3O Source Promotion Scope

Stage 3O is documentation and source-promotion work. It uses no CUDA, GPU acceleration, live Discord APIs, scraping, web crawling, AI upload, or benchmark claims. Generated promotion and Wiki sync reports remain ignored.

## Stage 2I Approval Readiness

Stage 2I is documentation and review-packet work only. The first real exploratory proposal records a bounded Caesar plus affine preview count, but it does not run on hardware, generate candidates, score output, or exercise CUDA.
# Stage 4Q Benchmark Planning

Stage 4Q records benchmark planning, not performance results. The `libreprimus benchmark-planning` CLI can write raw-data-free environment, CPU smoke, plan, readiness, and validation records. Generated diagnostics go under `experiments/results/benchmarks/stage4q/` and stay ignored.

Do not quote Stage 4Q smoke timing as a speed claim. Future CUDA work must still pass explicit CPU/GPU parity tests and benchmark gates.

# Stage 5A CUDA Planning

Stage 5A records CUDA target plans, explicit non-targets, parity scaffolds, and implementation gates. It does not compile CUDA kernels, run GPU benchmarks, or make speedup claims.

Stage 5B records CUDA parity harness plans, parity fixtures, backend capability profiles, and future-kernel matrix rows. It does not compile CUDA kernels, run GPU benchmarks, require the optional local 16GB GPU profile, or make speedup claims.

Stage 5E kernel-contract work cites Stage 5A target records, Stage 5B harness records, Stage 5C
build/device records, Stage 5D native CPU parity records, Stage 5F synthetic parity records, and
Stage 5G parity/device-code audit records. Stage 5F implementation must remain synthetic-only and
target the selected `shift_score_kernel` contract unless an explicit later stage revises the
contract.

Stage 5H adds the Gematria Primus mod-29 `shift_score` contract and native synthetic fixture
metadata. It records the production token-domain expectations for future parity work, but it does
not execute CUDA, run GPU benchmarks, process real Liber Primus data through CUDA, or make speedup
claims.

Stage 5J adds one synthetic numeric CUDA kernel for the Stage 5H fixture. Treat the passed local
build/parity record as correctness metadata only. It is not a benchmark, not a speedup claim, and
not permission to run solved or unsolved page data through CUDA.

Stage 5K converts the Stage 5J correctness metadata into committed parity/preflight records. Treat
the parity report, device-code audit, solved-fixture-safe blockers, and score-summary preflight as
readiness metadata only. They are not benchmarks, speedup claims, or permission to run solved or
unsolved page data through CUDA.

Stage 5L converts committed solved-fixture-safe streams into Gematria token buffers and native
output-token hashes. Treat those hashes as future parity fixtures only. They are not benchmarks,
speedup claims, CUDA execution evidence, or permission to run solved or unsolved page data through
CUDA.

Stage 5M records exact CUDA/native hash parity over the five Stage 5L buffers. Treat the local CUDA
run status and CTest result as bounded correctness metadata only. It is still not a benchmark,
speedup claim, broad CUDA implementation, or permission to run additional solved or unsolved page
data through CUDA.

Stage 5N reports the Stage 5M parity records and controlled expansion gates. It does not run CUDA
and must not be cited as performance evidence.

Stage 5O repeats only the exact Stage 5M solved-fixture-safe CUDA pack and records result-store
preflight. It is repeat correctness metadata, not a benchmark or speedup claim.

Stage 5R runs only the three Stage 5Q mapped direct-translation solved-fixture-safe candidates and
matches their native hashes. It is expanded correctness parity only, not a benchmark, speedup
claim, broad CUDA implementation, or permission to run unsolved page data through CUDA.

Stage 5T classifies solved-family CUDA readiness without running CUDA or benchmarks. Treat its
inventory, parity matrix, kernel-readiness ranking, ABI gaps, benchmark-readiness records, and
next-stage decision as planning metadata only. The selected next work is Stage 5U unified candidate
batch ABI consolidation, not benchmark execution or more shift-score widening.

Stage 5U defines Candidate Batch ABI v0, token-buffer, transform-parameter, key-schedule,
stream-schedule, score-vector, top-k, backend-surface, result-store compatibility, and ABI-gap
closure records. Treat these as no-GPU-safe contracts for future adapters only. Stage 5U does not
run CUDA, native/CUDA builds, solved or unsolved page inputs, benchmarks, or speedup measurements.
Stage 5U selected Stage 5V native candidate batch ABI reference adapter and conformance fixtures.

Stage 5V records native Candidate Batch ABI adapter metadata, seven raw-data-free conformance
fixtures, three Python reference output-token hashes, token-buffer conformance, schedule shape
conformance, score-vector/top-k conformance, and compact result-store conformance. Treat these as
no-GPU correctness metadata only. Stage 5V does not run CUDA, native/CUDA builds, solved or unsolved
page inputs, benchmarks, or speedup measurements. Stage 5W through Stage 5Y have since superseded
that decision; the selected next work is Stage 5Z prime-minus-one CUDA contract preparation, still
without kernel implementation, CUDA execution, benchmarks, or speedup measurements.

Stage 5Y consumes Stage 5X prime-minus-one no-GPU native parity records and writes compact reporting,
result-store, score-summary, method-status, generated-body policy, full-p56 blocker, CUDA contract
readiness-gate, bounded scored-experiment readiness, guardrail, and next-stage decision records.
Treat these as reporting and contract-preparation metadata only. Stage 5Y does not rerun native
parity, run CUDA, modify CUDA source, add kernels, execute full p56, benchmark, publish generated
bodies, or make solve claims.
