# Stage 5D Deterministic Threading Summary

Stage 5D tested deterministic threading for the native CPU backend over thread counts `1`, `2`, `4`,
`8`, and `16`.

All thread counts produced the same output hash:

`76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66`

The threading model uses range partitioning and fixed output slots. Timing is diagnostic only; the
records are not benchmarks and do not support speedup claims.
