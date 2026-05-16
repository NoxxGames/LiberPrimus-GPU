# Prime-Minus-One And Phi-Prime

## Purpose

This document describes the CPU-only Stage 1D known-solved fixture transform for p56. It is not a search module.

## Z_29 Domain

The transform uses Gematria profile v0 index values over `Z_29`.

## Prime Sequence

The fixture uses the prime sequence starting at prime index `0`: `2, 3, 5, 7, ...`.

## Phi Of Primes

For prime `p`, `phi(p)=p-1`. Therefore the phi-prime stream and prime-minus-one stream are equivalent for this fixture.

## Decryption Formula

`decoded_index = (cipher_index - ((prime_i - 1) mod 29)) mod 29`

## Stream Advancement

The stream advances only when an enciphered rune token is decoded. Separators, numeric literals, payload tokens, whitespace, and unknown symbols do not advance it.

## Skip Rule

Fixtures may declare a cleartext-F pass-through rule. Stage 1D uses it only for explicit fixture token indices and records the skip count.

## Worked Synthetic Example

With first stream value `(2-1) mod 29 = 1`, cipher index `1` decodes to `0`, which is Latin label `F`.

## Known Solved Fixture

`p56-an-end-prime-minus-one` passes with 84 prime values consumed, one cleartext-F skip, and a passing payload check.

## Non-Goals

No offset search, reverse search, prime-gap stream, scoring, CUDA, or generic transform registry is implemented here.

## Tests

Stage 1D tests cover first-prime generation, phi equivalence, stream advancement, payload checks, synthetic reproduction, CLI behaviour, and real-source conditional reproduction.
