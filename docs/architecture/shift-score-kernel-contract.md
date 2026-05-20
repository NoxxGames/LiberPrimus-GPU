# shift_score Kernel Contract

The `shift_score_kernel` contract is the first CUDA implementation target selected by Stage 5E and
implemented in synthetic-only form by Stage 5F.

## Contract Inputs

- Selected kernel: `shift_score_kernel`
- Selected target: `stage5a-caesar_mod29-cuda-target`
- Transform family label: `caesar_mod29`
- Adapter family: `native_cpu_synthetic_shift_adapter`
- Fixture: `stage5d-native-synthetic-shift-fixture-v0`

The Stage 5F kernel intentionally follows the Stage 5D native synthetic adapter, which shifts only
uppercase Latin alphabetic characters over 26 letters and preserves spaces. The contract name keeps
the future transform-family lineage, but the Stage 5F implementation is not production mod-29
Gematria behavior.

## Acceptance

A Stage 5F parity record is accepted only when the CUDA output hash matches the Stage 5D native
reference hash for the synthetic fixture. Skipped no-GPU records are valid for CI but are not parity
passes.

Future solved-fixture or production work must use a later explicit stage with new records and tests.
