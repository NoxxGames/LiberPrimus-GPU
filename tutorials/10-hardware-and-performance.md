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
