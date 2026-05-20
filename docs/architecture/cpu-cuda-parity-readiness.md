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

## Deferred CUDA State

CUDA remains deferred. Existing CUDA code is smoke/scaffold infrastructure unless a future explicit stage adds CPU/GPU parity tests, benchmark plans, and gated kernels.

## Non-Targets

Stage 4O parity readiness does not make hash cracking, stego/audio extraction, OCR, AI/ML image interpretation, or raw data processing CUDA targets.
