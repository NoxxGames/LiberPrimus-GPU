# Stage 5M Solved-Fixture CUDA Parity Summary

Stage 5M ran the existing `gematria_mod29_shift_score_kernel` over the exact five Stage 5L mapped solved-fixture-safe token buffers.

Counts:

- input mapping records: `5`;
- run records: `5`;
- CUDA attempted/pass/fail/skip: `5/5/0/0`;
- parity records: `5`;
- parity pass/fail/skip: `5/0/0`;
- boundary records: `1`;
- `stage5n_ready: true`.

All CUDA output-token hashes matched the Stage 5L native output-token hashes. The run did not process unsolved pages or real Liber Primus raw data and did not make a solve claim.
