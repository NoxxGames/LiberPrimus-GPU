# Solved-Fixture CUDA Boundaries

Solved-fixture CUDA execution is allowed only when a stage explicitly names the fixture set, kernel, expected hash contract, and no-unsolved boundary.

For Stage 5M the approved boundary is:

- exactly five Stage 5L mapped solved-fixture-safe token buffers;
- the existing `gematria_mod29_shift_score_kernel`;
- `gematria_shift_score_only` semantics;
- candidate shifts already recorded by Stage 5L native parity;
- candidate-major output ordering;
- comparison against Stage 5L native output-token hashes.

The boundary explicitly excludes:

- unsolved pages;
- raw Liber Primus page text;
- canonical corpus material;
- raw Discord logs;
- raw page images;
- raw stego or audio artifacts;
- GPU benchmarking and speedup claims.

The Stage 5M boundary record also captures that the CUDA source modification is host-runner-only. The device kernel arithmetic remains unchanged, and no new CUDA kernel is introduced.

Future CUDA stages must cite the Stage 5M summary and boundary records before widening solved-fixture coverage. Broad CUDA acceleration remains deferred until parity and benchmark planning gates are explicit.

Stage 5N boundary review preserves these limits and records that the parity pass authorizes only a future exact-repeat gate unless a later stage explicitly scopes more. Stage 5O consumes that exact-repeat gate and keeps the same boundary: no CUDA source changes, no new kernels, no benchmarks, and no unsolved-page data.
