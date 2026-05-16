# Explicit-Key Vigenere

## Purpose

This document defines the CPU-only explicit-key Vigenere transform used by Stage 1C solved fixtures.

## Z_29 Domain

The transform operates on Gematria profile v0 indices `0..28`.

## Gematria Profile Dependency

Key text and decoded labels use `data/profiles/gematria/gematria-primus-v0.json`.

## Formula

`decoded_index = (cipher_index - key_index[key_position]) mod 29`

## Key Conversion

The fixture key is parsed through Gematria profile Latin labels. No key search, inference, or length detection is performed.

## Key Advancement

The key advances only on enciphered rune tokens. Separators, numeric literals, whitespace, and unknown symbols do not advance the key.

## Separator Handling

Separator normalization follows the solved-fixture plaintext policy: word separators become spaces, clause separators become `. `, and line separators are joined.

## Cleartext F Skip Rule

Fixtures may declare `cleartext_f_pass_through`. Stage 1C real fixtures include explicit pass-through token indices so ordinary cipher `F` tokens are not skipped accidentally.

## Worked Synthetic Example

With key `U` (`index29=1`), cipher index `1` decrypts to `0`, which is `F`.

## Known Solved-Page Fixtures

- `welcome-divinity-vigenere`
- `a-koan-during-firfumferenfe-vigenere`

## Non-Goals

This implementation is not a Vigenere search engine, scoring system, CUDA kernel, or p56 prime-stream transform.

## Tests

Tests cover key conversion, subtract decryption, key advancement, separator handling, cleartext-F skip behaviour, fixture validation, CLI commands, and real-source reproduction.

## Future Relation To Vigenere Search

Any future search stage must build on this explicit-key CPU reference and add separate manifests, controls, null baselines, and review criteria.
