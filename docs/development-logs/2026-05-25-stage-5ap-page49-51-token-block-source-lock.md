# Stage 5AP Page 49-51 Token-Block Source Lock

Stage 5AP adds metadata-only source-lock and preflight infrastructure for the page 49-51 token block and OutGuess controls.

Implemented:

- `libreprimus token-block` CLI and `python/libreprimus/token_block/`.
- `libreprimus stego-controls` CLI and `python/libreprimus/stego_controls/`.
- Token-block, stego-control, and project-state schemas.
- Committed source-lock, image-provenance, transcription, coordinate, alphabet, mapping, null-control, DWH, OutGuess, research-summary, next-stage, and aggregate summary YAML records.
- Tests for schemas, transcription, coordinates, alphabet, mapping, null controls, DWH context, provenance, OutGuess toolchain/matrix/guardrails, next-stage decision, CLI, and ignore policy.

Local Stage 5AP summary counts: 15 page-image metadata records, 32 rows, 8 columns, 256 tokens, 161 unique tokens, 256 coordinate records, primary alphabet length 60, observed suffix count 59, null controls 5, OutGuess matrix records 5, historical fixtures ready 0.

Guardrails: no Deep Research execution, no raw image commit, no OCR, no AI/ML interpretation, no broad image forensics, no LP-page OutGuess, no hash/preimage search, no CUDA execution, no benchmarks, no scored experiments, no canonical corpus activation, no page-boundary finalisation, and no solve claim.
