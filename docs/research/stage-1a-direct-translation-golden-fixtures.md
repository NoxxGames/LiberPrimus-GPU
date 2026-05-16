# Stage 1A Direct-Translation Golden Fixtures

## Status

Stage 1A adds solved-page golden fixtures for direct translation only. The fixtures are test expectations, not new solve claims.

## Stage Goal

The goal is to prove that known direct-translation solved material can be reproduced from Stage 0E profiles and the inactive rtkd corpus candidate.

## Inputs

- rtkd master transcript lock: `rtkd-master-transcription`
- scream314 solved-page reference lock: `scream314-liber-primus-md`
- Gematria profile: `gematria-primus-v0`
- Separator grammar: `rtkd-separator-grammar-v0`
- Glyph variant profile: `glyph-variants-v0`
- Corpus candidate: `rtkd-master-v0-candidate`

## Direct-Translation Scope

Stage 1A covers `The Loss of Divinity`, `Some Wisdom`, `An Instruction`, and `p57 Parable` as direct Gematria-profile transliterations.

## Out-of-Scope Methods

Atbash, reverse Gematria, Vigenere, rotated reverse Gematria, prime streams, brute force, scoring, and CUDA acceleration are not implemented in this stage.

## Fixture Provenance

Every fixture records source transcript SHA-256, solved-reference SHA-256, profile SHA-256s, corpus candidate ID, fixture version, and non-canonical flags.

## Normalized Plaintext Policy

The decoder emits uppercase preferred Latin labels from `gematria-primus-v0`. Word separators become spaces, clause separators become `. `, visual line separators are joined, numeric literals are preserved, repeated whitespace collapses, and leading/trailing whitespace is trimmed.

## Fixture Results

The real Stage 1A smoke currently has four fixtures, all passing direct translation reproduction.

## Pending/Ambiguous Fixtures

No direct-translation fixture is pending in Stage 1A. Future non-direct solved pages remain out of scope.

## What This Stage Proves

It proves the current profiles, candidate token records, span selectors, and direct decoder can reproduce selected known direct-transliteration material deterministically.

## What This Stage Does Not Prove

It does not activate a canonical corpus, finalize page boundaries, solve unsolved pages, or validate non-direct solved-page methods.

## Next Stage

Stage 1B should add reverse Gematria / Atbash-family reproduction only for clearly documented solved pages.
