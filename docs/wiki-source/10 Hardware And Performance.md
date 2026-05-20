> This Wiki page mirrors $sourceRel. The repository tutorial file is the source of truth.

# Hardware And Performance

## CPU/GPU Responsibility Split

CPU code owns corpus management, manifests, orchestration, provenance, branching search, and review.

GPU code will later accelerate large regular transform-and-score batches only after CPU references and parity tests exist.

Stage 2E dry-run manifests may estimate future CPU candidate counts, but they do not run benchmarks, execute search, or use CUDA. Treat those counts as planning metadata only.

## Current Stage

Stage 0D-P does not use CUDA. Transcript parsing and alignment run on ordinary CPU hardware.

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
