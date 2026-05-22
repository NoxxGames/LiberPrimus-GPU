# Stage 5W Prime-Minus-One Native Contract

Date: 2026-05-22

## Scope

Stage 5W prepares the prime-minus-one stream family for a later no-GPU native parity execution stage. It consumes Stage 5V Candidate Batch ABI conformance records, Stage 5U stream-schedule contracts, and committed p56 solved-fixture-safe metadata.

## Implementation

- Added `libreprimus prime-minus-one-native-contract`.
- Added source inventory, stream contract, prime schedule, Candidate Batch ABI mapping, native parity preparation, result-store preflight, guardrail, next-stage decision, and summary records.
- Recorded the source-backed p56 formula direction, skip policy, and bounded Stage 4O/5L two-token mapping.
- Kept full p56 fixture parity blocked because a full committed p56 cipher token buffer is not present.

## Local Results

- Source inventory records: `7`
- Stream contract records: `2`
- Prime schedule records: `3`
- Candidate batch mapping records: `3`
- Native parity preparation records: `3`
- Result-store preflight records: `3`
- Guardrail records: `6`
- Next-stage decision records: `8`

## Guardrails

No CUDA was run. No CUDA source was modified. No kernels were added. No native/CUDA CMake build was run. No benchmark, speedup claim, unsolved-page CUDA, real Liber Primus CUDA-data use, raw-data processing, generated-body publication, website expansion, method-status upgrade, canonical corpus activation, page-boundary finalisation, or solve claim was made.

## Next

Stage 5X - prime-minus-one stream no-GPU native parity execution and result-store preflight.
