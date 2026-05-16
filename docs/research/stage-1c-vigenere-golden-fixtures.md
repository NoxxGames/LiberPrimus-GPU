# Stage 1C Vigenere Golden Fixtures

## Status

Stage 1C is implemented as a known-solved baseline stage. It does not solve new pages, activate a canonical corpus, or finalize page boundaries.

## Stage Goal

Stage 1C mirrors additional reference sources, locks their hashes, and reproduces two documented explicit-key Vigenere solved sections through the solved-fixture framework.

## Inputs

- Stage 0E Gematria profile v0, separator grammar v0, and glyph-variant profile v0.
- Generated `rtkd-master-v0-candidate` corpus candidate outputs.
- Locked rtkd and scream314 transcript references.
- Mirrored reference-only files from `scream314/cicada3301` and `lipeeeee/gematria`.

## Reference Sources Mirrored

The mirrored raw files live under ignored `data/raw/reference-repos/`. Lock metadata is committed under `data/locks/reference-repos/`.

Stage 1C locked `9` reference files: `3` from `scream314/cicada3301` and `6` from `lipeeeee/gematria`.

## Vigenere Scope

Only explicit-key Vigenere fixture reproduction is in scope:

- `welcome-divinity-vigenere`, key `DIVINITY`.
- `a-koan-during-firfumferenfe-vigenere`, key `FIRFUMFERENFE`.

## Out-Of-Scope Methods

No key search, key inference, scoring, CUDA, prime-stream, p56, generic affine search, or unsolved-page solving is implemented.

## Method Formula

For enciphered rune tokens:

`decoded_index = (cipher_index - key_index[key_position]) mod 29`

The key position advances only for enciphered rune tokens.

## Key Handling

Fixture key text is converted through Gematria profile v0 Latin labels. `DIVINITY` resolves to `[23, 10, 1, 10, 9, 10, 16, 26]`; `FIRFUMFERENFE` resolves to `[0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18]`.

## Skip-Rule Handling

The cleartext-F pass-through rule is fixture-declared. Stage 1C uses explicit token indices because the locked spans contain cipher `F` tokens that are not all cleartext `F`.

## Fixture Provenance

Each Vigenere fixture includes source transcript SHA-256, solved-reference SHA-256, method-reference SHA-256, profile SHA-256s, corpus candidate id, fixture version, and non-canonical flags.

## Normalized Plaintext Policy

Output uses the Stage 1A profile-label normalization: uppercase preferred Latin labels, word separators as spaces, clause separators as `. `, joined line separators, numeric literals preserved, and trimmed whitespace.

## Fixture Results

Real-source Vigenere reproduction result: `2/0/0/0` pass/fail/pending/skipped.

## Direct Fixture Regression

Stage 1C smoke keeps Stage 1A direct fixtures passing at `4/0/0/0`.

## Atbash Fixture Regression

Stage 1C smoke keeps Stage 1B Atbash-family fixtures passing at `3/0/0/0`.

## Pending/Ambiguous Fixtures

No Vigenere fixtures are pending in Stage 1C. The fixtures still mark spans as reviewable and page boundaries as non-final.

## What This Stage Proves

The current profiles and generated corpus candidate can reproduce two documented explicit-key Vigenere known-solved baselines with declared skip rules.

## What This Stage Does Not Prove

It does not prove any new solution, validate unsolved pages, activate a canonical corpus, finalize page boundaries, or implement Vigenere search.

## Next Stage

Recommended next stage: Stage 1D - reproduce p56 An End prime-minus-one / phi-prime solved-page behaviour with preserved payload checks.
