# CPU Reference Transform Registry

## Purpose

This page lists the transforms registered for solved-baseline reproduction in Stage 2A.

## Registered Transforms

- `direct_translation`
- `reverse_gematria`
- `rotated_reverse_gematria`
- `vigenere_explicit_key`
- `prime_minus_one_stream`
- `phi_prime_stream` as an alias of `prime_minus_one_stream`

## Formulas

- `direct_translation`: `decoded_index = cipher_index`
- `reverse_gematria`: `decoded_index = 28 - cipher_index`
- `rotated_reverse_gematria`: `decoded_index = (28 - cipher_index + rotation) mod 29`
- `vigenere_explicit_key`: `decoded_index = (cipher_index - key_index[key_position]) mod 29`
- `prime_minus_one_stream`: `decoded_index = (cipher_index - ((prime_i - 1) mod 29)) mod 29`
- `phi_prime_stream`: `phi(p)=p-1` for prime `p`, implemented through `prime_minus_one_stream`

## Parameters

Parameters must be explicit. Rotated reverse fixtures declare `rotation`; Vigenere fixtures declare `key_text` and direction; prime-stream fixtures declare `prime_start_index`, direction, stream value, and any skip rule.

## Alias Rules

Aliases resolve to canonical transform IDs before dispatch. Alias entries do not enable additional campaign families.

## Fixture Coverage

- `direct_translation`: `direct-translation-v0`
- `reverse_gematria`, `rotated_reverse_gematria`: `atbash-family-v0`
- `vigenere_explicit_key`: `vigenere-v0`
- `prime_minus_one_stream`, `phi_prime_stream`: `prime-stream-v0`

## Non-Goals

Stage 2A does not implement generic affine search, Caesar sweeps, Vigenere key search, prime-stream offset search, scoring, or CUDA kernels.

## Future Transforms

New transforms should first be CPU reference implementations with parameter schemas, fixture controls, provenance, and tests.
