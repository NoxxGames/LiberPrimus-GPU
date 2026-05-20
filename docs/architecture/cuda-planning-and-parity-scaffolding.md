# CUDA Planning And Parity Scaffolding

Stage 5A is a planning-only CUDA boundary. It converts Stage 4Q CUDA parity readiness into target-plan records, non-target records, parity scaffold records, and implementation gates.

No CUDA source, GPU kernel, GPU benchmark, speedup claim, raw-data processing, broad experiment, canonical corpus activation, page-boundary finalisation, or solve claim is part of Stage 5A.

The planning chain is:

- Stage 4O supplies CPU batch parity expectations and deterministic output hashes.
- Stage 4P supplies unified result surfaces for cross-stage score/status comparison.
- Stage 4Q supplies CPU benchmark planning and CUDA parity readiness.
- Stage 5A records which targets are ready for planning, blocked, or out of CUDA scope.

Stage 5B cites the Stage 5A records to create a harness skeleton, parity fixtures, backend capability profiles, and future-kernel matrix rows. Stage 5C then records CUDA build and device-detection metadata. Stage 5D records native C++ CPU backend and deterministic threading parity records. Planning, harness, build/device, and native CPU readiness are not execution readiness.

## Committed Records

- `data/cuda/stage5a-cuda-target-plan.yaml`
- `data/cuda/stage5a-cuda-non-targets.yaml`
- `data/cuda/stage5a-cuda-parity-scaffold.yaml`
- `data/cuda/stage5a-cuda-implementation-gates.yaml`
- `data/cuda/stage5a-cuda-planning-summary.yaml`

Generated JSON reports remain ignored under `experiments/results/cuda-planning/stage5a/`.

Stage 5B generated CUDA parity reports remain ignored under `experiments/results/cuda-parity/stage5b/`; committed Stage 5B records live under `data/cuda/`. Stage 5C generated CUDA build/device reports remain ignored under `experiments/results/cuda-build/stage5c/`; committed Stage 5C records live under `data/cuda/`. Stage 5D generated native CPU reports remain ignored under `experiments/results/native-cpu/stage5d/`; committed Stage 5D records live under `data/native-cpu/`.
