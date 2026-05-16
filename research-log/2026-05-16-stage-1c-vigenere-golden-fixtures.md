# Stage 1C Vigenere Golden Fixtures Research Log

## Status

Stage 1C reproduces explicit-key Vigenere known-solved fixtures only. It is not a new solve stage.

## Reference Sources

Stage 1C mirrors and locks `scream314/cicada3301` and `lipeeeee/gematria` files as reference/provenance inputs only. Raw mirrored files remain ignored.

## Method

The Vigenere transform uses Gematria profile v0 over `Z_29`:

`decoded_index = (cipher_index - key_index[key_position]) mod 29`

The key advances only on enciphered rune tokens. Cleartext-F pass-through is fixture-declared and records explicit token indices.

## Fixtures

- `welcome-divinity-vigenere`, key `DIVINITY`, logical lines `31..53`.
- `a-koan-during-firfumferenfe-vigenere`, key `FIRFUMFERENFE`, logical lines `289..321`.

Both fixtures pass with generated outputs ignored.

## Regression

Direct fixtures remain `4/0/0/0`; Atbash-family fixtures remain `3/0/0/0`.

## Limits

No canonical corpus is activated. Page boundaries remain reviewable. No key search, scoring, CUDA, p56 prime stream, or generic affine machinery is implemented.

## Next Stage

Stage 1D should reproduce p56 An End prime-minus-one / phi-prime solved-page behaviour if locked references support the fixture.
