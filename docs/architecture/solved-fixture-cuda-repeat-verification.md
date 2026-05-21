# Solved-Fixture CUDA Repeat Verification

Stage 5P follow-up: compact Stage 5O repeat parity metadata is now integrated into
Stage 4P/Stage 4I-compatible result-store and score-summary records. Generated CUDA result bodies
remain ignored and unpublished.

Stage 5O repeats only the exact Stage 5M Gematria solved-fixture-safe CUDA parity pack. The input
surface is the same five Stage 5L mapped token buffers and candidate-shift lists that Stage 5M used.

The repeat verifier compares each Stage 5O CUDA output-token hash against two committed references:

- the Stage 5L native output-token hash;
- the Stage 5M CUDA output-token hash.

A repeat parity record is `passed` only when both comparisons match. The stage adds no CUDA kernels,
does not modify CUDA source, does not benchmark, does not process unsolved-page data, and does not
publish generated result bodies.
