# Stage 5U - CUDA Candidate Batch ABI

Date: 2026-05-22

Stage 5U consumes the Stage 5T solved-family CUDA readiness matrix and records a shared Candidate Batch ABI v0 for future native and CUDA backend work. The stage is metadata-first and no-GPU-safe: no CUDA was run, no native/CUDA build was required, no CUDA/C++ implementation files were changed, no benchmarks were run, no generated result bodies were published, and no solve claim was made.

Implemented records:

- Candidate Batch ABI v0.
- Token-buffer contracts for header, token values, token kinds, transformable mask, separators, fixture offsets, fixture lengths, and fixture references.
- Transform-parameter contracts for `shift_mod29`, reverse Gematria, rotated reverse Gematria, affine mod-29, explicit-key Vigenere, and prime-minus-one stream families.
- Key-schedule and stream-schedule contracts.
- Stage 4I-compatible score-vector and deterministic top-k output contracts.
- Backend-surface contracts for Python orchestration, native reference, CUDA host/device, result-store, score-summary, and generated-body policy boundaries.
- Stage 4P result-store compatibility records.
- Stage 5T ABI gap closure records.
- Stage 5V next-stage decision records.

Validation focus:

- Stage 5U records must remain contract metadata and must reject CUDA execution, CUDA source changes, kernel additions, GPU benchmarks, generated-output publication, raw-data processing, website expansion, method-status upgrades to solved, and solve claims.
- The selected next stage is `Stage 5V - native candidate batch ABI reference adapter and conformance fixtures`.
- Generated reports remain under ignored `experiments/results/cuda-candidate-batch-abi/stage5u/`.
- The detailed completion handoff remains under ignored `codex-output/stage5u-codex-completion.md`.
