# Stage 1D p56 Prime-Stream Golden Fixture

## Status

Stage 1D is a known-solved fixture reproduction stage. It does not solve new pages, activate a canonical corpus, finalize page boundaries, add search, or use CUDA.

## Stage Goal

Reproduce p56 `An End` using the locked Stage 0E profiles, the generated rtkd corpus candidate, and locked scream314 method references.

## Inputs

- Gematria profile: `data/profiles/gematria/gematria-primus-v0.json`
- Separator grammar: `data/profiles/separators/rtkd-separator-grammar-v0.json`
- Glyph variant profile: `data/profiles/glyph-variants/glyph-variants-v0.json`
- Corpus candidate: `rtkd-master-v0-candidate`
- Solved reference: `data/raw/transcripts/scream314/liber_primus.md`
- Method reference: `data/raw/reference-repos/scream314-cicada3301/pages_and_ciphers.md`

## p56 Scope

The only Stage 1D fixture is `p56-an-end-prime-minus-one`. It uses explicit logical lines `1690..1710` from the Stage 0E candidate and keeps the span `reviewable`.

## Out-Of-Scope Methods

Stage 1D does not implement prime-stream search, offset sweeps, reverse direction sweeps, prime-gap streams, scoring, CUDA, or generic affine/shift/search infrastructure.

## Method Formula

For the ith enciphered rune token, using the ith prime `q_i` from the declared start index:

`decoded_index = (cipher_index - ((q_i - 1) mod 29)) mod 29`

## Prime-Minus-One / Phi-Prime Equivalence

For prime `p`, `phi(p) = p - 1`. Stage 1D records `phi_prime_stream` as an alias for `prime_minus_one_stream` rather than a separate search family.

## Stream Advancement Rules

The stream advances only on enciphered rune tokens. Separators, numeric literals, payload tokens, whitespace, and unknown symbols do not advance the stream.

## Cleartext-F Skip Rule

The p56 fixture declares a cleartext-F pass-through skip rule with explicit token index `22202`. The skip emits `F`, does not advance the stream, and is recorded in reproduction output.

## Payload Preservation

The p56 hex block is extracted from logical lines `1697..1705`, normalized as exact hex lines, and hash-checked separately from plaintext.

## Fixture Provenance

The fixture records source transcript SHA-256, solved-reference SHA-256, method-reference SHA-256, profile SHA-256s, corpus candidate ID, `canonical_corpus_active=false`, `page_boundaries_final=false`, and `trusted_as_canonical=false`.

## Normalized Plaintext Policy

Decoded runes emit Gematria profile preferred Latin labels. Word separators become spaces, clause separators become `. `, repeated whitespace collapses, and payload text is omitted from plaintext.

## Fixture Results

Prime-stream fixtures: `1/0/0/0` pass/fail/pending/skipped. Payload check: `pass`.

## Regressions

Direct fixtures remain `4/0/0/0`, Atbash-family fixtures remain `3/0/0/0`, and Vigenere fixtures remain `2/0/0/0`.

## What This Stage Proves

Known p56 solved material can be reproduced by the current profile/candidate fixture framework.

## What This Stage Does Not Prove

It does not prove canonical corpus activation, final page boundaries, new solved pages, or search correctness.

## Next Stage

Recommended next stage: Stage 2A CPU transform registry and manifest-addressable solved-baseline runner.
