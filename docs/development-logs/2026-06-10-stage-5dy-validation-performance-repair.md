# Stage 5DY - Validation Performance Repair

Date: 2026-06-10

Stage 5DY repairs validation performance, parallel-test discipline, stage-isolation, shared-schema collision risk, and non-mutating validator policy before the third Source Browser number-fact review batch.

Implementation notes:

- Added Stage 5DY records, schemas, CLI validators, focused tests, and summary commands.
- Added staged validation profiles: focused, stage-fast, local-fast, full-parallel, full-serial-rare, and CI.
- Added `scripts/ci/run-stage-validation.*` and repaired consistency/parallel-validation scripts so local development can use focused or fast profiles before broad parallel validation.
- Preserved the Stage 5CM-and-later 8-worker cap and kept the old 16-worker default from returning.
- Recorded Stage 5DX slow-validation diagnostics as summarized metadata, not raw pasted output.
- Added stage-isolation policy so historical validators avoid mutable global Source Browser counts.
- Added shared-schema collision policy so stage-specific schemas do not overwrite shared schema paths.
- Added non-mutating validator policy and focused regression coverage for representative validate/summary commands.
- Updated ChatGPT/context docs so future prompts avoid repeated full serial pytest loops unless a concrete fallback reason exists.

Guardrails preserved:

- Stage 5DX records remain preserved.
- Stage 5BD run-plan IDs remain `10`.
- Active-lineage records remain `8`.
- No number-fact batch 3 was performed.
- No historical source-lock records were rewritten.
- No target was selected.
- No route extraction, byte generation, OCR, image/audio/stego analysis, community-code execution, native/VM/spreadsheet execution, Tor/network target access, CUDA, scoring, benchmark, or solve claim was performed.
