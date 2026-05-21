# Stage 5M Solved-Fixture CUDA Parity

Stage 5M runs the existing Gematria mod-29 `shift_score` CUDA kernel over the five Stage 5L solved-fixture-safe mapped token buffers.

Local result:

- run records: `5`;
- CUDA attempted: `5`;
- CUDA pass/fail/skip: `5/0/0`;
- parity records: `5`;
- parity pass/fail/skip: `5/0/0`;
- boundary records: `1`;
- `stage5n_ready: true`.

All five CUDA output-token hashes matched the Stage 5L native hashes. The generated run reports remain ignored under `experiments/results/gematria-solved-fixture-cuda/stage5m/`.

This stage does not exercise the source transform semantics for reverse Gematria, rotated reverse, Vigenere, or prime-stream families. It exercises only mapped numeric `shift_score` buffers.

No GPU benchmark was run, no performance or speedup claim was made, no unsolved page data was processed, and no solve claim was made.
