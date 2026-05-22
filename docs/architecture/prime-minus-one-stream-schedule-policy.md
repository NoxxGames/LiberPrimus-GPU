# Prime-Minus-One Stream Schedule Policy

Prime-minus-one stream schedules are deterministic records, not generated search evidence.

## Rules

- Generate primes deterministically from the declared start index.
- Convert each stream value with `(prime_i - 1) mod 29`.
- Advance only on enciphered rune tokens.
- Do not advance on separators, payload tokens, or explicit skip tokens.
- Preserve cleartext-F skip policy exactly where the committed fixture declares it.
- Do not invent token values, page spans, plaintext, ciphertext, or stream formulas.

Stage 5W may write compact schedule metadata and ignored JSON reports. Generated bodies stay ignored.
