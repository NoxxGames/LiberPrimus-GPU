# Hardware And Performance

## CPU/GPU Responsibility Split

CPU code owns corpus management, manifests, orchestration, provenance, branching search, and review.

GPU code will later accelerate large regular transform-and-score batches only after CPU references and parity tests exist.

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
