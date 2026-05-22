# CUDA Key And Stream Schedule Contracts

Stage 5U defines contract records for explicit-key and prime-stream schedule surfaces.

## Key Schedules

The explicit-key Vigenere schedule uses Gematria token keys `0..28`, per-candidate key references, declared reset policy, and declared advance policy. Separators do not advance keys. Dictionary-scale key batches remain out of scope.

## Stream Schedules

The prime-minus-one schedule uses declared deterministic stream values `(prime_i - 1) mod 29`, per-candidate start indexes, and declared reset/advance policy. The `phi_prime_stream` alias is represented as a prime-minus-one stream alias where records declare it.

Arbitrary integer streams are blocked until a future source-backed family contract defines them.
