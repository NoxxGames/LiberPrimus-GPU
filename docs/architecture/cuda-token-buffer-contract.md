# CUDA Token Buffer Contract

Stage 5U records token-buffer contracts for Candidate Batch ABI v0.

## Required Buffers

- `token_buffer_header_v0`: count and offset metadata.
- `token_values_buffer`: signed token values, with runes `0..28` and separator sentinel `-1`.
- `token_kind_buffer`: rune, payload, separator, and unknown-preserved token kinds.
- `transformable_mask_buffer`: one byte per token; separators must be `0`.
- `separator_position_buffer`: optional validation surface for separator positions.
- `fixture_offset_buffer` and `fixture_length_buffer`: fixture-to-token spans.
- `candidate_fixture_reference_buffer`: candidate-major fixture references.

These are contracts only. Native and CUDA conformance tests must prove byte layout, ordering, separator behavior, and output-token hash compatibility before execution widening.
