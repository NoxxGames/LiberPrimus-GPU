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

CUDA remains deferred. Stage 5A is CUDA planning and parity scaffolding only. Existing CUDA code is smoke/scaffold infrastructure unless a future explicit stage adds CPU/GPU parity tests, benchmark plans, and gated kernels.

## Non-Targets

Stage 4O and Stage 4P parity readiness do not make hash cracking, stego/audio extraction, OCR, AI/ML image interpretation, generated result publication, or raw data processing CUDA targets.
