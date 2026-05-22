# Stage 5W Prime Stream Contract Summary

Stage 5W records the prime-minus-one stream contract as a source-backed native parity preparation surface.

- Contract family: `prime_minus_one_stream`
- Formula direction: source-backed from committed solved-fixture/reference records
- Stream value: `(prime_i - 1) mod 29`
- Decryption direction: subtract the stream value from ciphertext tokens modulo 29
- Prime index base: zero-based deterministic schedule records
- Advance policy: enciphered rune tokens only
- Separator policy: separators and skipped cleartext markers do not advance the stream

The stage does not execute native parity or CUDA. It prepares records for a future no-GPU native run.
