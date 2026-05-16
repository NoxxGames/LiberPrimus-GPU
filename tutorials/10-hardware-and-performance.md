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
