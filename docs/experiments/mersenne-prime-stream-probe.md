# Mersenne prime stream probe

Stage 3G added `stage3i_mersenne_prime_stream_tiny_v1` to the backlog and bounded queue as a low-cost stream-family falsification probe. Stage 3J implements and runs the bounded probe through `stage3j_mersenne_prime_stream_tiny_v1`.

## Rationale

The evidence level is `weak_to_moderate`: Cicada material uses primes, binary-style processing, Gematria prime values, and p56 uses a prime-derived stream. Mersenne-derived streams are adjacent enough to justify a tiny future probe, but not strong enough to outrank p56-local and reset/advance work.

## Planned Parameters

- Exponents: `2`, `3`, `5`, `7`, `13`, `17`, `19`, `31`
- Variants: `mersenne_mod29`, `mersenne_minus_one_mod29`, `perfect_number_mod29`
- Offsets: `0..15`
- Directions: `forward`, `reverse`
- Reset modes: `none`, `line`
- Candidate count: `3 * 16 * 2 * 2 = 192`

## Status

Stage 3J executes all `192` candidates with `0` deferred. Because the eight-exponent sequence is cyclic, the run reports duplicate stream signatures: `96` unique signatures and `96` duplicate signatures.

The top lead is `perfect_number_mod29`, offset `3`, direction `forward`, reset `none`, score `1.515716`, calibrated confidence `inconclusive`. This is not solve evidence.

Generated outputs remain ignored under `experiments/results/bounded-auto-runs/stage3j/`.
