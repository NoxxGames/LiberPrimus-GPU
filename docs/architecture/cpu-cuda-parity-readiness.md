# CPU/CUDA Parity Readiness

Stage 4O adds a parity-readiness layer on top of the Stage 4H CPU batch contract and the Stage 4I scoring contract. It is a CPU reference record set, not CUDA implementation.

## Required Future CUDA Anchors

Future CUDA work must match CPU records for:

- input stream token order;
- separator preservation;
- unknown-token behavior;
- transform parameter hashes;
- output token hashes;
- output text hashes where applicable;
- score-summary shape and scorer metadata.

CUDA results are not trustworthy until they match Stage 4O parity expectations and pass explicit CPU/GPU tests.

## Stage 4P Reporting Layer

Stage 4P records a unified result surface over CPU batch outputs, score summaries, method statuses, and retirement states. Stage 4Q records CPU benchmark and parity readiness gates. Future CUDA readiness should cite Stage 4O parity expectation hashes, Stage 4P unified result records, and Stage 4Q readiness records before benchmarks or kernels are considered comparable.

## Deferred CUDA State

CUDA remains deferred. Stage 5A CUDA planning and parity scaffolding is complete, Stage 5B CUDA parity harness skeleton is complete, Stage 5C CUDA build/device detection is complete, and Stage 5D native C++ CPU batch backend and deterministic threading baseline is complete. Stage 5E first CUDA kernel contract and CPU/native parity adapter selection is next. Existing CUDA code is smoke/scaffold infrastructure unless a future explicit stage adds CPU/GPU parity tests, benchmark plans, and gated kernels.

Stage 5D records native output hashes and deterministic threading parity for the synthetic fixture.
Those records are readiness inputs, not CUDA execution, benchmark, or speedup evidence.

Stage 5A converts Stage 4O, Stage 4P, and Stage 4Q references into explicit CUDA target-plan and parity scaffold records. Stage 5B converts those records into harness plans, parity fixtures, backend capability profiles, and future-kernel matrix rows. Stage 5C records no-GPU-safe build profiles, toolchain records, optional device metadata, and smoke-build status. Readiness means a future implementation can be planned; it does not mean a CUDA implementation exists or may be benchmarked.

## Non-Targets

Stage 4O and Stage 4P parity readiness do not make hash cracking, stego/audio extraction, OCR, AI/ML image interpretation, generated result publication, or raw data processing CUDA targets.
