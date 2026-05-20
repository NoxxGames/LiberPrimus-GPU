# Deterministic Threading For Parity

Stage 5D uses deterministic range partitioning and fixed output slots for native CPU batch work.
Threading changes execution scheduling only; it must not change record ordering, output text, output
hashes, score shape, or provenance flags.

## Rules

- Candidate order is stable and sorted by candidate index.
- Each candidate writes to its preassigned output slot.
- Thread ranges are derived from candidate count and requested thread count.
- One-thread and multi-thread runs must produce the same output hash.
- Timing fields are diagnostics only and are not benchmarks or speedup claims.

The Stage 5D threading records cover thread counts `1`, `2`, `4`, `8`, and `16` for the synthetic
fixture. All produce the same output hash:

`76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66`

Future CUDA parity work should treat these hashes as reference behavior, not as performance targets.
