# Mersenne prime stream probe

Stage 3G adds `stage3i_mersenne_prime_stream_tiny_v1` to the future backlog and bounded queue as a low-cost stream-family falsification probe.

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

The probe is queued as `needs_executor` / dry-run-only and is not executed in Stage 3G. It must remain bounded, documented, CPU-only, and generated-output-ignored when a future stage implements it.
